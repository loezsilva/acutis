from datetime import datetime, timedelta, timezone
from dateutil.relativedelta import relativedelta
import logging
from uuid import uuid4
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


class CreatePixPayment:
    def __init__(self, payment_setup_id: int) -> None:
        self.__payment_setup = payment_setup_id

    def execute(self):
        METHODS_MAP = {
            1: self.__itau_create_payment,
            2: self.__mercado_pago_payment,
        }

        payment_gateway = METHODS_MAP[self.__payment_setup]
        return payment_gateway()

    def __itau_create_payment(self):
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
            nome = current_user["nome"]

            if periodicidade not in [1, 2]:
                response = {
                    "error": "Valor de periodicidade inválido: 1 - Única, 2 - Mensal."
                }
                log_access(
                    response,
                    current_user["id"],
                    current_user["nome"],
                    current_user["fk_perfil_id"],
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
                )
                return response, 404

            clifor = db.session.get(Clifor, current_user["fk_clifor_id"])

            reference_num = f"{current_user['id']}_PIX_{datetime.timestamp(datetime.now())}"

            data_vencimento = (
                get_current_time() + relativedelta(months=1)
            ).strftime("%Y-%m-%d")

            TxID = uuid4().hex
            path_put = f"/cobv/{TxID}"
            path_get = path_put + "/qrcode"
            devedor = (
                {"cpf": cpf_cnpj, "nome": nome}
                if len(cpf_cnpj) == 11
                else {"cnpj": cpf_cnpj, "nome": nome}
            )

            body = {
                "calendario": {
                    "dataDeVencimento": data_vencimento,
                    "validadeAposVencimento": 0,
                },
                "devedor": devedor,
                "valor": {"original": valor_doacao},
                "chave": campanha.chave_pix,
            }

            itau_api = ItauAPI("pix")

            response_put, status_put = itau_api.put(path=path_put, body=body)
            response_get, status_get = itau_api.get(path=path_get)

            if status_put != 201 or status_get != 200:
                logging.error(f"RESPONSE PUT ----> {response_put}")
                logging.error(f"RESPONSE GET ----> {response_get}")

                if (
                    response_put.get("violacoes", [])[0].get("razao")
                    == "Chave não encontrada na DICT"
                ):
                    return {
                        "error": "A chave pix cadastrada na campanha é inválida."
                    }, 400

                response = {
                    "error": "Ocorreu um erro ao criar o pagamento via pix!"
                }
                log_access(
                    response,
                    current_user["id"],
                    current_user["nome"],
                    current_user["fk_perfil_id"],
                )
                return response, 500

            register_order(
                campanha=campanha,
                clifor=clifor,
                reference_num=reference_num,
                valor_doacao=valor_doacao,
                forma_pagamento=2,
                periodo=periodicidade,
                id_pedido=None,
                id_transacao=TxID,
                fk_gateway_pagamento_id=self.__payment_setup,
            )

            response = {
                "msg": "Pix gerado com sucesso.",
                "pix_qrcode": response_get.get("emv"),
                "qr_code_base64": response_get.get("imagem_base64"),
            }

            print(response)

            log_access(
                response,
                current_user["id"],
                current_user["nome"],
                current_user["fk_perfil_id"],
                201,
            )

            return response, 201

        except KeyError as err:
            logging.error(err)
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
            logging.error(err)
            return {"error": "Ocorreu um erro ao gerar o pagamento."}, 500

    def __mercado_pago_payment(self):
        try:
            payload = request.get_json()

            periodicidade = payload["periodicidade"]
            fk_campanha_id = payload["fk_campanha_id"]
            valor_doacao = payload["valor_doacao"]
            if float(valor_doacao) < 10:
                return {
                    "error": "O valor mínimo a ser doado é de 10 reais."
                }, 400

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

            reference_num = f"{current_user['id']}_PIX_MPAG_{datetime.timestamp(datetime.now())}"

            clifor = db.session.get(Clifor, current_user["fk_clifor_id"])

            if (campanha := db.session.get(Campanha, fk_campanha_id)) is None:
                response = {"error": "Campanha não encontrada."}
                log_access(
                    response,
                    current_user["id"],
                    current_user["nome"],
                    current_user["fk_perfil_id"],
                    400,
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
                    400,
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
                "payment_method_id": "pix",
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
                forma_pagamento=2,
                periodo=periodicidade,
                id_pedido=None,
                id_transacao=mp_data.get("id"),
                fk_gateway_pagamento_id=self.__payment_setup,
            )

            response = {
                "msg": "Pix gerado com sucesso.",
                "pix_qrcode": mp_data.get("point_of_interaction")
                .get("transaction_data")
                .get("qr_code"),
                "qr_code_base64": mp_data.get("point_of_interaction")
                .get("transaction_data")
                .get("qr_code_base64"),
            }

            log_access(
                response,
                current_user["id"],
                current_user["nome"],
                current_user["fk_perfil_id"],
                201,
            )

            return response, 201

        except MercadoPagoException as exception:
            error = translator.translate(exception.error_message)
            return {
                "error": str(error),
            }, exception.status_code

        except KeyError as ex:
            return {"error": f"O campo {ex} é obrigatório."}, 400

        except Exception as ex:
            logging.error(ex)
            return {
                "error": "Ocorreu um erro ao criar o pagamento.",
            }, 500
