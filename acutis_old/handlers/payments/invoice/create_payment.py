from datetime import datetime, timedelta, timezone
from dateutil.relativedelta import relativedelta
import logging
import random

from flask import request
from flask_jwt_extended import current_user

from exceptions.exception_mercado_pago import MercadoPagoException
from models.campanha import Campanha
from models.clifor import Clifor
from models.endereco import Endereco
from services.itau_api import ItauAPI
from services.mercado_pago_api import MercadoPago
from utils.checkout import register_order
from utils.functions import get_current_time
from utils.logs_access import log_access
from builder import db, translator


class CreateInvoicePayment:
    def __init__(self, payment_setup_id: int) -> None:
        self.__payment_setup = payment_setup_id

    def execute(self):
        METHODS_MAP = {1: self.__itau_payment, 2: self.__mercado_pago_payment}

        payment_gateway = METHODS_MAP[self.__payment_setup]
        return payment_gateway()

    def __itau_payment(self):
        try:
            payload = request.get_json()

            valor_doacao = payload["valor_doacao"]
            if float(valor_doacao) < 10:
                return {
                    "error": "O valor mínimo a ser doado é de 10 reais."
                }, 400
            fk_campanha_id = payload["fk_campanha_id"]
            periodicidade = payload["periodicidade"]
            nome = current_user["nome"]
            cpf_cnpj = current_user["numero_documento"]

            if (
                endereco := Endereco.query.filter_by(
                    fk_clifor_id=current_user["fk_clifor_id"]
                ).first()
            ) is None:
                response = {"error", f"Endereço não encontrado."}
                log_access(
                    response,
                    current_user["id"],
                    current_user["nome"],
                    current_user["fk_perfil_id"],
                    404,
                )
                return response, 404

            if periodicidade not in [1, 2]:
                response = {
                    "error": "Valor de periodicidade inválido: 1 - Única, 2 - Mensal."
                }
                log_access(
                    response,
                    current_user["id"],
                    current_user["nome"],
                    current_user["fk_perfil_id"],
                    400,
                )
                return response, 400

            if (campanha := db.session.get(Campanha, fk_campanha_id)) is None:
                response = {
                    "error": f"Campanha com id {fk_campanha_id} não encontrada."
                }
                log_access(
                    response,
                    current_user["id"],
                    current_user["nome"],
                    current_user["fk_perfil_id"],
                    404,
                )
                return response, 404

            clifor = db.session.get(Clifor, current_user["fk_clifor_id"])

            reference_num = f"{current_user['id']}_BOLETO_{datetime.timestamp(datetime.now())}"

            valor_boleto = str(int(valor_doacao * 100)).zfill(17)

            data_vencimento = (
                get_current_time() + relativedelta(months=1)
            ).strftime("%Y-%m-%d")

            numero_nosso_numero = random.randrange(10**7, 10**8)

            path = "/boletos_pix"

            tipo_pessoa = (
                {
                    "codigo_tipo_pessoa": "F",
                    "numero_cadastro_pessoa_fisica": cpf_cnpj,
                }
                if len(cpf_cnpj) == 11
                else {
                    "codigo_tipo_pessoa": "J",
                    "numero_cadastro_nacional_pessoa_juridica": cpf_cnpj,
                }
            )

            body = {
                "etapa_processo_boleto": "efetivacao",
                "beneficiario": {"id_beneficiario": "382700998646"},
                "dado_boleto": {
                    "tipo_boleto": "a vista",
                    "codigo_carteira": "109",
                    "valor_total_titulo": valor_boleto,
                    "codigo_especie": "99",
                    "data_emissao": datetime.now().strftime("%Y-%m-%d"),
                    "pagador": {
                        "pessoa": {
                            "nome_pessoa": nome,
                            "tipo_pessoa": tipo_pessoa,
                        },
                        "endereco": {
                            "nome_logradouro": (
                                endereco.rua
                                if len(endereco.rua) <= 45
                                else endereco.rua[:45]
                            ),
                            "nome_bairro": (
                                endereco.bairro
                                if len(endereco.bairro) <= 15
                                else endereco.bairro[:15]
                            ),
                            "nome_cidade": (
                                endereco.cidade
                                if len(endereco.cidade) <= 20
                                else endereco.cidade[:20]
                            ),
                            "sigla_UF": (
                                endereco.estado
                                if len(endereco.estado) <= 2
                                else endereco.estado[:2]
                            ),
                            "numero_CEP": endereco.cep,
                        },
                    },
                    "sacador_avalista": {
                        "pessoa": {
                            "nome_pessoa": "INSTITUTO HESED DOS IRMAOS E IRMAS",
                            "tipo_pessoa": {
                                "codigo_tipo_pessoa": "J",
                                "numero_cadastro_nacional_pessoa_juridica": "02779337000174",
                            },
                        },
                        "endereco": {
                            "nome_logradouro": "AVENIDA DIONISIO LEONEL ALENCAR",
                            "nome_bairro": "ANCURI",
                            "nome_cidade": "FORTALEZA",
                            "sigla_UF": "CE",
                            "numero_CEP": "60873073",
                        },
                    },
                    "dados_individuais_boleto": [
                        {
                            "numero_nosso_numero": numero_nosso_numero,
                            "data_vencimento": data_vencimento,
                            "valor_titulo": valor_boleto,
                            "data_limite_pagamento": data_vencimento,
                        }
                    ],
                },
                "dados_qrcode": {"chave": campanha.chave_pix},
            }

            itau_api = ItauAPI("bolecode")

            data, status = itau_api.post(path=path, body=body)

            if status != 200:
                logging.error(f"RESPONSE POST ----> {data}")
                response = {
                    "error": "Ocorreu um erro ao criar o boleto de pagamento."
                }
                log_access(
                    response,
                    current_user["id"],
                    current_user["nome"],
                    current_user["fk_perfil_id"],
                    503,
                )
                return response, 503

            response = data["data"]
            response["msg"] = "Boleto gerado com sucesso."

            TxID = response["dados_qrcode"]["txid"]
            nosso_numero = response["dado_boleto"]["dados_individuais_boleto"][
                0
            ]["numero_nosso_numero"]

            register_order(
                campanha=campanha,
                clifor=clifor,
                reference_num=reference_num,
                valor_doacao=valor_doacao,
                forma_pagamento=3,
                periodo=periodicidade,
                id_pedido=None,
                id_transacao=TxID,
                nosso_numero=nosso_numero,
                fk_gateway_pagamento_id=self.__payment_setup,
            )

            log_access(
                response,
                current_user["id"],
                current_user["nome"],
                current_user["fk_perfil_id"],
            )
            return response, 201

        except KeyError as err:
            response = {"error": f"O campo {err} é obrigatório."}
            log_access(
                response,
                current_user["id"],
                current_user["nome"],
                current_user["fk_perfil_id"],
                400,
            )
            return response, 400

        except Exception as err:
            response = {
                "error": "Ocorreu um erro ao criar o boleto de pagamento.",
                "type_error": f"{type(err)}",
                "msg_error": str(err),
            }, 500
            log_access(
                response,
                current_user["id"],
                current_user["nome"],
                current_user["fk_perfil_id"],
            )
            return response

    def __mercado_pago_payment(self):
        try:
            payload = request.get_json()

            valor_doacao = payload["valor_doacao"]
            if float(valor_doacao) < 10:
                return {
                    "error": "O valor mínimo a ser doado é de 10 reais."
                }, 400
            fk_campanha_id = payload["fk_campanha_id"]
            periodicidade = payload["periodicidade"]

            cpf_cnpj = current_user["numero_documento"]
            email = current_user["email"]
            nome = current_user["nome"]

            first_name = nome.split(" ")[0]
            last_name = nome.split(" ")[-1]

            tipo_documento = "CPF" if len(cpf_cnpj) == 11 else "CNPJ"

            if periodicidade not in [1, 2]:
                response = {
                    "error": "Valor de periodicidade inválido: 1 - Única, 2 - Mensal."
                }
                log_access(
                    response,
                    current_user["id"],
                    current_user["nome"],
                    current_user["fk_perfil_id"],
                    400,
                )
                return response, 400

            reference_num = f"{current_user['id']}_BOLETO_MPAG_{datetime.timestamp(datetime.now())}"

            clifor = db.session.get(Clifor, current_user["fk_clifor_id"])

            if (campanha := db.session.get(Campanha, fk_campanha_id)) is None:
                response = {"error": "Campanha não encontrada."}
                log_access(
                    response,
                    current_user["id"],
                    current_user["nome"],
                    current_user["fk_perfil_id"],
                    404,
                )
                return response, 404

            if (
                endereco := Endereco.query.filter_by(
                    fk_clifor_id=clifor.id
                ).first()
            ) is None:
                response = {"error", "Endereço não encontrado."}
                log_access(
                    response,
                    current_user["id"],
                    current_user["nome"],
                    current_user["fk_perfil_id"],
                    404,
                )
                return response, 404

            dt = (
                (datetime.now(tz=timezone.utc) + timedelta(days=31))
                if periodicidade == 2
                else (datetime.now(tz=timezone.utc) + timedelta(weeks=1))
            )
            date_of_expiration = dt.strftime("%Y-%m-%dT%H:%M:%S.%f")[
                :-3
            ] + dt.strftime("%z")

            payment_payload = {
                "transaction_amount": valor_doacao,
                "description": f"Doação para a campanha {campanha.titulo}",
                "payment_method_id": "bolbradesco",
                "date_of_expiration": date_of_expiration,
                "payer": {
                    "email": email,
                    "first_name": first_name,
                    "last_name": last_name,
                    "identification": {
                        "type": tipo_documento,
                        "number": cpf_cnpj,
                    },
                    "address": {
                        "zip_code": endereco.cep,
                        "street_name": endereco.rua,
                        "street_number": endereco.numero,
                        "neighborhood": endereco.bairro,
                        "city": endereco.cidade,
                        "federal_unit": endereco.estado,
                    },
                },
            }

            mp = MercadoPago()
            mp_data = mp.create_payment(payment_payload)

            register_order(
                campanha=campanha,
                clifor=clifor,
                reference_num=reference_num,
                valor_doacao=valor_doacao,
                forma_pagamento=3,
                periodo=periodicidade,
                id_pedido=None,
                id_transacao=mp_data.get("id"),
                fk_gateway_pagamento_id=self.__payment_setup,
            )

            mp_data["msg"] = "Boleto gerado com sucesso."

            log_access(
                mp_data,
                current_user["id"],
                current_user["nome"],
                current_user["fk_perfil_id"],
                201,
            )

            return mp_data, 201
        except MercadoPagoException as exception:
            error = translator.translate(exception.error_message)
            return {
                "error": str(error),
            }, exception.status_code

        except KeyError as ex:
            return {"error": f"O campo {ex} é obrigatório."}, 400

        except Exception as ex:
            return {
                "error": "Ocorreu um erro ao criar o pagamento.",
                "type_error": str(type(ex)),
                "msg_error": str(ex),
            }, 500
