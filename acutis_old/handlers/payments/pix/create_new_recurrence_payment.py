from datetime import datetime, timedelta, timezone
from dateutil.relativedelta import relativedelta
import logging
from uuid import uuid4
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


class CreateNewPixRecurrencePayment:
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
            1: self.__itau_create_new_pix_payment,
            2: self.__mercado_pago_create_new_pix_payment,
        }

        new_pix_payment = METHODS_MAP[self.__fk_gateway_pagamento_id]

        return new_pix_payment()

    def __itau_create_new_pix_payment(self):
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

            DEVEDOR_MAP = {
                11: {"cpf": clifor.cpf_cnpj, "nome": clifor.nome},
                14: {"cnpj": clifor.cpf_cnpj, "nome": clifor.nome},
            }

            data_vencimento = (
                get_current_time() + relativedelta(months=1)
            ).strftime("%Y-%m-%d")

            TxID = uuid4().hex
            path_put = f"/cobv/{TxID}"
            path_get = path_put + "/qrcode"
            devedor = DEVEDOR_MAP[len(clifor.cpf_cnpj)]

            body = {
                "calendario": {
                    "dataDeVencimento": data_vencimento,
                    "validadeAposVencimento": 0,
                },
                "devedor": devedor,
                "valor": {"original": float(processamento_pedido.valor)},
                "chave": campanha.chave_pix,
            }

            itau_api = ItauAPI("pix")

            response_put, status_put = itau_api.put(path=path_put, body=body)
            response_get, status_get = itau_api.get(path=path_get)

            if status_put != 201:
                return {
                    "error": "Ocorreu um erro ao gerar o pagamento.",
                    "type_error": str(status_put),
                    "msg_error": str(response_put),
                }, 500

            if status_get != 200:
                return {
                    "error": "Ocorreu um erro ao retornar os dados de pagamento",
                    "type_error": str(status_get),
                    "msg_error": str(response_get),
                }, 500

            processamento_pedido.data_processamento = get_current_time()
            processamento_pedido.transaction_id = TxID

            db.session.commit()

            response = {
                "msg": "Pix gerado com sucesso.",
                "pix_qrcode": response_get.get("emv"),
                "qr_code_base64": response_get.get("imagem_base64"),
            }

            return response, 201

        except Exception as exception:
            logging.error(str(exception))
            return {
                "error": "Ocorreu um erro ao gerar um novo pagamento."
            }, 500

    def __mercado_pago_create_new_pix_payment(self):
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
                "payment_method_id": "pix",
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
            response_mp = mp.create_payment(payment_payload)

            processamento_pedido.data_processamento = get_current_time()
            processamento_pedido.transaction_id = response_mp.get("id")

            db.session.commit()

            response = {
                "msg": "Pix gerado com sucesso.",
                "pix_qrcode": response_mp.get("point_of_interaction", {})
                .get("transaction_data", {})
                .get("qr_code"),
                "qr_code_base64": response_mp.get("point_of_interaction", {})
                .get("transaction_data", {})
                .get("qr_code_base64"),
            }

            return response, 201
        except MercadoPagoException as exception:
            logging.error(str(exception))
            return {
                "error": "Ocorreu um erro ao gerar o pagamento."
            }, exception.status_code

        except Exception as exception:
            db.session.rollback()
            logging.error(str(exception))
            return {"error": "Ocorreu um erro ao criar o pagamento."}, 500
