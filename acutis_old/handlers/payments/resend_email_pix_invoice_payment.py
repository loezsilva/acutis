import logging
from flask_jwt_extended import current_user
from exceptions.exception_mercado_pago import MercadoPagoException
from models.campanha import Campanha
from models.clifor import Clifor
from models.pedido import Pedido
from models.processamento_pedido import ProcessamentoPedido
from models.usuario import Usuario
from services.factories import file_service_factory
from services.itau_api import ItauAPI
from services.mercado_pago_api import MercadoPago
from templates.email_templates import (
    recurrence_pix_invoice_payment_email_template,
)
from utils.send_email import send_email
from utils.logs_access import log_access
from utils.token_email import generate_token
from builder import translator


class ResendEmailPixInvoicePayment:
    def __init__(
        self,
        transaction_id: int,
        fk_gateway_pagamento_id: int,
        fk_forma_pagamento_id: int,
    ) -> None:
        self.__transaction_id = transaction_id
        self.__fk_gateway_pagamento_id = fk_gateway_pagamento_id
        self.__fk_forma_pagamento_id = fk_forma_pagamento_id

    def execute(self):
        METHODS_MAP = {
            1: {
                2: self.__itau_resend_pix_payment,
                3: self.__itau_resend_invoice_payment,
            },
            2: {
                2: self.__mercado_pago_resend_pix_payment,
                3: self.__mercado_pago_resend_invoice_payment,
            },
        }

        resend_payment = METHODS_MAP.get(
            self.__fk_gateway_pagamento_id, {}
        ).get(self.__fk_forma_pagamento_id)
        return resend_payment()

    def __itau_resend_pix_payment(self):
        try:
            if (
                payload := (
                    ProcessamentoPedido.query.join(
                        Pedido, Pedido.id == ProcessamentoPedido.fk_pedido_id
                    )
                    .join(Campanha, Campanha.id == Pedido.fk_campanha_id)
                    .join(Clifor, Clifor.id == Pedido.fk_clifor_id)
                    .join(Usuario, Usuario.id == Clifor.fk_usuario_id)
                    .filter(
                        ProcessamentoPedido.transaction_id
                        == self.__transaction_id
                    )
                    .filter(ProcessamentoPedido.fk_forma_pagamento_id == 2)
                    .filter(Pedido.periodicidade == 2)
                    .with_entities(
                        ProcessamentoPedido.transaction_id,
                        ProcessamentoPedido.status_processamento,
                        ProcessamentoPedido.fk_forma_pagamento_id,
                        Pedido.recorrencia_ativa,
                        Pedido.fk_gateway_pagamento_id,
                        Campanha.id.label("fk_campanha_id"),
                        Campanha.titulo,
                        Campanha.filename,
                        Usuario.nome,
                        Usuario.email,
                    )
                    .first()
                )
            ) is None:
                return {"error": "Pedido de pagamento não encontrado."}, 404

            if payload.status_processamento != 0:
                return {"error": "Pedido de pagamento já processado."}, 403

            if payload.recorrencia_ativa != 1:
                return {
                    "error": "Pedido de pagamento não possui recorrência ativa."
                }, 403

            itau_api = ItauAPI("pix")

            get_status_payment, status_code = itau_api.get(
                path=f"/cobv/{payload.transaction_id}"
            )

            if status_code not in [200, 201, 204]:
                response = {"error": "Ocorreu um erro ao buscar o pagamento."}
                log_access(
                    response,
                    current_user["id"],
                    current_user["nome"],
                    current_user["fk_perfil_id"],
                )
                return response, 500

            if get_status_payment["status"] != "ATIVA":
                return {"error": "Este pagamento não está mais ativo."}, 400

            s3_client = file_service_factory()

            foto_campanha = s3_client.get_public_url(payload.filename)

            obj = {
                "transaction_id": payload.transaction_id,
                "fk_gateway_pagamento_id": self.__fk_gateway_pagamento_id,
            }

            token = generate_token(
                obj=obj, salt="send_email_pix_recurrence_payment"
            )
            template = recurrence_pix_invoice_payment_email_template(
                name=payload.nome,
                campanha_id=payload.fk_campanha_id,
                nome_campanha=payload.titulo,
                token=token,
                tipo_pagamento="pix",
                foto_campanha=foto_campanha,
            )

            send_email(
                "Reenvio de pagamento recorrente", payload.email, template, 3
            )

            return {"msg": "Pedido de pagamento reenviado com sucesso."}, 200

        except:
            return {
                "error": "Ocorreu um erro ao reenviar o pedido de pagamento."
            }, 500

    def __itau_resend_invoice_payment(self):
        try:
            if (
                payload := (
                    ProcessamentoPedido.query.join(
                        Pedido, Pedido.id == ProcessamentoPedido.fk_pedido_id
                    )
                    .join(Campanha, Campanha.id == Pedido.fk_campanha_id)
                    .join(Clifor, Clifor.id == Pedido.fk_clifor_id)
                    .join(Usuario, Usuario.id == Clifor.fk_usuario_id)
                    .filter(
                        ProcessamentoPedido.transaction_id
                        == self.__transaction_id
                    )
                    .filter(ProcessamentoPedido.fk_forma_pagamento_id == 3)
                    .filter(Pedido.periodicidade == 2)
                    .with_entities(
                        ProcessamentoPedido.transaction_id,
                        ProcessamentoPedido.status_processamento,
                        ProcessamentoPedido.fk_forma_pagamento_id,
                        ProcessamentoPedido.nosso_numero,
                        Pedido.recorrencia_ativa,
                        Pedido.fk_gateway_pagamento_id,
                        Campanha.id.label("fk_campanha_id"),
                        Campanha.titulo,
                        Campanha.filename,
                        Usuario.nome,
                        Usuario.email,
                    )
                    .first()
                )
            ) is None:
                return {"error": "Pedido de pagamento não encontrado."}, 404

            if payload.status_processamento != 0:
                return {"error": "Pedido de pagamento já processado."}, 403

            if payload.recorrencia_ativa != 1:
                return {
                    "error": "Pedido de pagamento não possui recorrência ativa."
                }, 403

            itau_api = ItauAPI("pix")

            get_status_payment, status_code = itau_api.get(
                path=f"/cobv/{payload.transaction_id}"
            )

            if status_code not in [200, 201, 204]:
                response = {"error": "Ocorreu um erro ao buscar o pagamento."}
                log_access(
                    response,
                    current_user["id"],
                    current_user["nome"],
                    current_user["fk_perfil_id"],
                )
                return response, 500

            if get_status_payment["status"] != "ATIVA":
                return {"error": "Este pagamento não está mais ativo."}, 400

            s3_client = file_service_factory()

            foto_campanha = s3_client.get_public_url(payload.filename)

            obj = {
                "transaction_id": payload.nosso_numero,
                "fk_gateway_pagamento_id": self.__fk_gateway_pagamento_id,
            }

            token = generate_token(
                obj=obj, salt="send_email_invoice_recurrence_payment"
            )
            template = recurrence_pix_invoice_payment_email_template(
                name=payload.nome,
                campanha_id=payload.fk_campanha_id,
                nome_campanha=payload.titulo,
                token=token,
                tipo_pagamento="invoice",
                foto_campanha=foto_campanha,
            )

            send_email(
                "Reenvio de pagamento recorrente", payload.email, template, 3
            )

            return {"msg": "Pedido de pagamento reenviado com sucesso."}, 200

        except Exception as ex:
            logging.error(ex)
            return {
                "error": "Ocorreu um erro ao reenviar o pedido de pagamento."
            }, 500

    def __mercado_pago_resend_pix_payment(self):
        try:
            if (
                payload := (
                    ProcessamentoPedido.query.join(
                        Pedido, Pedido.id == ProcessamentoPedido.fk_pedido_id
                    )
                    .join(Campanha, Campanha.id == Pedido.fk_campanha_id)
                    .join(Clifor, Clifor.id == Pedido.fk_clifor_id)
                    .join(Usuario, Usuario.id == Clifor.fk_usuario_id)
                    .filter(
                        ProcessamentoPedido.transaction_id
                        == self.__transaction_id
                    )
                    .filter(ProcessamentoPedido.fk_forma_pagamento_id == 2)
                    .filter(Pedido.periodicidade == 2)
                    .with_entities(
                        ProcessamentoPedido.transaction_id,
                        ProcessamentoPedido.status_processamento,
                        ProcessamentoPedido.fk_forma_pagamento_id,
                        Pedido.recorrencia_ativa,
                        Pedido.fk_gateway_pagamento_id,
                        Campanha.id.label("fk_campanha_id"),
                        Campanha.titulo,
                        Campanha.filename,
                        Usuario.nome,
                        Usuario.email,
                    )
                    .first()
                )
            ) is None:
                return {"error": "Pedido de pagamento não encontrado."}, 404

            if payload.status_processamento != 0:
                return {"error": "Pedido de pagamento já processado."}, 403

            if payload.recorrencia_ativa != 1:
                return {
                    "error": "Pedido de pagamento não possui recorrência ativa."
                }, 403

            mp = MercadoPago()

            response_mp = mp.get_payment(payload.transaction_id)

            if response_mp.get("status") != "pending":
                return {"error": "Este pagamento não está mais ativo."}, 400

            s3_client = file_service_factory()

            foto_campanha = s3_client.get_public_url(payload.filename)

            obj = {
                "transaction_id": payload.transaction_id,
                "fk_gateway_pagamento_id": self.__fk_gateway_pagamento_id,
            }

            token = generate_token(
                obj=obj, salt="send_email_pix_recurrence_payment"
            )
            template = recurrence_pix_invoice_payment_email_template(
                name=payload.nome,
                campanha_id=payload.fk_campanha_id,
                nome_campanha=payload.titulo,
                token=token,
                tipo_pagamento="pix",
                foto_campanha=foto_campanha,
            )

            send_email(
                "Reenvio de pagamento recorrente", payload.email, template, 3
            )

            return {"msg": "Pedido de pagamento reenviado com sucesso."}, 200

        except MercadoPagoException as exception:
            error = translator.translate(exception.error_message)
            response = {"error": error}
            log_access(
                response,
                current_user["id"],
                current_user["nome"],
                current_user["fk_perfil_id"],
            )
            return response, exception.status_code

        except Exception as exception:
            logging.error(exception)
            return {
                "error": "Ocorreu um erro ao reenviar o pedido de pagamento."
            }, 500

    def __mercado_pago_resend_invoice_payment(self):
        try:
            if (
                payload := (
                    ProcessamentoPedido.query.join(
                        Pedido, Pedido.id == ProcessamentoPedido.fk_pedido_id
                    )
                    .join(Campanha, Campanha.id == Pedido.fk_campanha_id)
                    .join(Clifor, Clifor.id == Pedido.fk_clifor_id)
                    .join(Usuario, Usuario.id == Clifor.fk_usuario_id)
                    .filter(
                        ProcessamentoPedido.transaction_id
                        == self.__transaction_id
                    )
                    .filter(ProcessamentoPedido.fk_forma_pagamento_id == 3)
                    .filter(Pedido.periodicidade == 2)
                    .with_entities(
                        ProcessamentoPedido.transaction_id,
                        ProcessamentoPedido.status_processamento,
                        ProcessamentoPedido.fk_forma_pagamento_id,
                        Pedido.recorrencia_ativa,
                        Pedido.fk_gateway_pagamento_id,
                        Campanha.id.label("fk_campanha_id"),
                        Campanha.titulo,
                        Campanha.filename,
                        Usuario.nome,
                        Usuario.email,
                    )
                    .first()
                )
            ) is None:
                return {"error": "Pedido de pagamento não encontrado."}, 404

            if payload.status_processamento != 0:
                return {"error": "Pedido de pagamento já processado."}, 403

            if payload.recorrencia_ativa != 1:
                return {
                    "error": "Pedido de pagamento não possui recorrência ativa."
                }, 403

            mp = MercadoPago()

            response_mp = mp.get_payment(payload.transaction_id)

            if response_mp.get("status") != "pending":
                return {"error": "Este pagamento não está mais ativo."}, 400

            s3_client = file_service_factory()

            foto_campanha = s3_client.get_public_url(payload.filename)

            obj = {
                "transaction_id": payload.transaction_id,
                "fk_gateway_pagamento_id": self.__fk_gateway_pagamento_id,
            }

            token = generate_token(
                obj=obj, salt="send_email_invoice_recurrence_payment"
            )
            template = recurrence_pix_invoice_payment_email_template(
                name=payload.nome,
                campanha_id=payload.fk_campanha_id,
                nome_campanha=payload.titulo,
                token=token,
                tipo_pagamento="invoice",
                foto_campanha=foto_campanha,
            )

            send_email(
                "Reenvio de pagamento recorrente", payload.email, template, 3
            )

            return {"msg": "Pedido de pagamento reenviado com sucesso."}, 200

        except MercadoPagoException as exception:
            error = translator.translate(exception.error_message)
            response = {"error": error}
            log_access(
                response,
                current_user["id"],
                current_user["nome"],
                current_user["fk_perfil_id"],
            )
            return response, exception.status_code

        except Exception as exception:
            logging.error(exception)
            return {
                "error": "Ocorreu um erro ao reenviar o pedido de pagamento."
            }, 500
