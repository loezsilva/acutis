from datetime import datetime, timedelta, timezone
from dateutil.relativedelta import relativedelta
import logging
import random

from flask import jsonify
from exceptions.exception_mercado_pago import MercadoPagoException
from models.campanha import Campanha
from models.clifor import Clifor
from models.endereco import Endereco
from models.pedido import Pedido
from models.processamento_pedido import ProcessamentoPedido
from models.usuario import Usuario

from builder import db
from services.itau_api import ItauAPI
from services.mercado_pago_api import MercadoPago
from utils.functions import get_current_time


class CreateNewInvoiceRecurrencePayment:
    def __init__(
        self,
        fk_usuario_id: int,
        fk_processamento_pedido_id: int,
        fk_pedido_id: int,
        fk_gateway_pagamento_id: int,
    ) -> None:
        self.__fk_usuario_id = fk_usuario_id
        self.__fk_processamento_pedido_id = fk_processamento_pedido_id
        self.__fk_pedido_id = fk_pedido_id
        self.__fk_gateway_pagamento_id = fk_gateway_pagamento_id

    def execute(self):
        METHODS_MAP = {
            1: self.__itau_create_new_invoice_payment,
            2: self.__mercado_pago_create_new_invoice_payment,
        }

        new_pix_payment = METHODS_MAP[self.__fk_gateway_pagamento_id]

        return new_pix_payment()

    def __itau_create_new_invoice_payment(self):
        try:
            usuario = db.session.get(Usuario, self.__fk_usuario_id)
            processamento_pedido = db.session.get(
                ProcessamentoPedido, self.__fk_processamento_pedido_id
            )
            pedido = db.session.get(Pedido, self.__fk_pedido_id)

            if processamento_pedido.status_processamento == 1:
                return {"error": "Pagamento já processado."}, 403

            campanha = db.session.get(Campanha, pedido.fk_campanha_id)
            if not campanha:
                return {"error": "Campanha para doação não encontrada."}, 404

            if not campanha.status:
                return {"error": "Esta campanha foi encerrada."}, 403

            clifor = Clifor.query.filter_by(fk_usuario_id=usuario.id).first()
            if not clifor:
                return {"error": "cliente não encontrado."}, 404

            endereco = Endereco.query.filter_by(fk_clifor_id=clifor.id).first()
            if not endereco:
                return {"error", "Endereço do usuário não encontrado."}, 404

            valor_boleto = str(int(processamento_pedido.valor * 100)).zfill(17)

            data_vencimento = (
                get_current_time() + relativedelta(months=1)
            ).strftime("%Y-%m-%d")

            numero_nosso_numero = random.randrange(10**7, 10**8)

            path = "/boletos_pix"

            TIPO_PESSOA_MAP = {
                11: {
                    "codigo_tipo_pessoa": "F",
                    "numero_cadastro_pessoa_fisica": clifor.cpf_cnpj,
                },
                14: {
                    "codigo_tipo_pessoa": "J",
                    "numero_cadastro_nacional_pessoa_juridica": clifor.cpf_cnpj,
                },
            }

            tipo_pessoa = TIPO_PESSOA_MAP[len(clifor.cpf_cnpj)]

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
                            "nome_pessoa": usuario.nome,
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

            resp, status = itau_api.post(path=path, body=body)

            if status != 200:
                logging.error(
                    f"type_error: {str(status)} - msg_error: {str(resp)}"
                )
                return {
                    "error": "Ocorreu um erro ao criar o boleto de pagamento."
                }, 500

            response = resp["data"]
            response["msg"] = "Boleto gerado com sucesso."

            TxID = response["dados_qrcode"]["txid"]
            nosso_numero = response["dado_boleto"]["dados_individuais_boleto"][
                0
            ]["numero_nosso_numero"]

            processamento_pedido.data_processamento = get_current_time()
            processamento_pedido.transaction_id = TxID
            processamento_pedido.nosso_numero = nosso_numero

            db.session.commit()

            return jsonify(response), 201

        except Exception as exception:
            logging.error(str(exception))
            return {
                "error": "Ocorreu um erro ao gerar um novo pagamento."
            }, 500

    def __mercado_pago_create_new_invoice_payment(self):
        try:
            usuario = db.session.get(Usuario, self.__fk_usuario_id)
            processamento_pedido = db.session.get(
                ProcessamentoPedido, self.__fk_processamento_pedido_id
            )
            pedido = db.session.get(Pedido, self.__fk_pedido_id)

            if processamento_pedido.status_processamento == 1:
                return {"error": "Pagamento já processado."}, 403

            campanha = db.session.get(Campanha, pedido.fk_campanha_id)
            if not campanha:
                return {"error": "Campanha para doação não encontrada."}, 404

            if not campanha.status:
                return {"error": "Esta campanha foi encerrada."}, 403

            clifor = Clifor.query.filter_by(fk_usuario_id=usuario.id).first()
            if not clifor:
                return {"error": "Cliente não encontrado."}, 404

            first_name = usuario.nome.split(" ")[0]
            last_name = usuario.nome.split(" ")[-1]

            tipo_documento = "CPF" if len(clifor.cpf_cnpj) == 11 else "CNPJ"

            if (
                endereco := Endereco.query.filter_by(
                    fk_clifor_id=clifor.id
                ).first()
            ) is None:
                response = {"error", "Endereço do cliente não encontrado."}
                return response, 404

            dt = datetime.now(tz=timezone.utc) + timedelta(days=31)
            date_of_expiration = dt.strftime("%Y-%m-%dT%H:%M:%S.%f")[
                :-3
            ] + dt.strftime("%z")

            payment_payload = {
                "transaction_amount": float(
                    round(processamento_pedido.valor, 2)
                ),
                "description": f"Doação para a campanha {campanha.titulo}",
                "payment_method_id": "bolbradesco",
                "date_of_expiration": date_of_expiration,
                "payer": {
                    "email": usuario.email,
                    "first_name": first_name,
                    "last_name": last_name,
                    "identification": {
                        "type": tipo_documento,
                        "number": clifor.cpf_cnpj,
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

            processamento_pedido.data_processamento = get_current_time()
            processamento_pedido.transaction_id = mp_data.get("id")

            db.session.commit()

            mp_data["msg"] = "Boleto gerado com sucesso."

            return mp_data, 201

        except MercadoPagoException as exception:
            logging.error(str(exception))
            return {
                "error": "Ocorreu um erro ao gerar o pagamento."
            }, exception.status_code

        except Exception as exception:
            db.session.rollback()
            logging.error(str(exception))
            return {"error": "Ocorreu um erro ao criar o pagamento."}, 500
