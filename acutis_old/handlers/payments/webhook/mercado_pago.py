from datetime import datetime
from flask import request
from models.clifor import Clifor
from models.pedido import Pedido
from models.processamento_pedido import ProcessamentoPedido
from services.mercado_pago_api import MercadoPago
from utils.mercado_pago import MercadoPagoUtils
from builder import db
from utils.functions import get_current_time


class MercadoPagoWebhook:
    def __init__(self, logger) -> None:
        self.logger = logger

    def execute(self) -> any:
        try:
            if not self.__validate_signature():
                self.logger.error({"msg": "Invalid signature"})
                return {}, 401

            data = request.get_json()
            return self.__handle_event(data)

        except Exception as err:
            db.session.rollback()
            self.logger.error(
                {
                    "error": "Ocorreu um erro ao salvar o pagamento.",
                    "errorMsg": f"{str(type(err))} - {str(err)}",
                    "requisicao": data,
                }
            )
            return {}, 500

    def __validate_signature(self):
        return MercadoPagoUtils.validate_signature(request)

    def __handle_event(self, data: dict) -> any:
        event_type = data.get("type")
        if event_type == "payment":
            return self.__handle_payment(data)
        elif event_type == "subscription_preapproval":
            return self.__handle_subscription_preapproval(data)
        elif event_type == "subscription_authorized_payment":
            return self.__handle_subscription_authorized_payment(data)
        return {}, 200

    def __handle_payment(self, data):
        data_id = data.get("data", {}).get("id")
        mp = MercadoPago()
        if data.get("action") not in ["payment.update", "payment.updated"]:
            return {}, 200

        processamento_pedido = self.__get_processamento_pedido(data_id)
        if processamento_pedido is None:
            self.logger.error(
                {"error": "Pagamento não encontrado.", "requisicao": data}
            )
            return {}, 200

        response = mp.get_payment(data_id)
        self.__update_processamento_pedido(processamento_pedido, response)
        return {}, 200

    def __handle_subscription_preapproval(self, data):
        data_id = data.get("data", {}).get("id")
        mp = MercadoPago()
        if data.get("action") == "updated":
            pedido = self.__get_pedido(data_id)
            if pedido is None:
                self.logger.error(
                    {"error": "Pedido não encontrado.", "requisicao": data}
                )
                return {}, 200

            response = mp.get_preapproval(data_id)
            if response.get("status") == "cancelled":
                pedido.recorrencia_ativa = False
                pedido.status_pedido = 2
                db.session.commit()

            return {}, 200

        return {}, 200

    def __handle_subscription_authorized_payment(self, data):
        data_id = data.get("data", {}).get("id")
        mp = MercadoPago()
        if data.get("action") == "updated":
            response = mp.get_authorized_payment(data_id)
            subscription_id = response.get("preapproval_id")
            status_payment = response.get("payment", {}).get("status")
            transaction_id = response.get("id")

            pedido = self.__get_pedido(subscription_id)
            if pedido is None:
                self.logger.error(
                    {
                        "gateway": "Mercado Pago",
                        "action-type": "Pagamento recorrente",
                        "msg": "Pedido não encontrado",
                        "data": data,
                    }
                )
                return {}, 200

            clifor = db.session.get(Clifor, pedido.fk_clifor_id)
            status_processamento = 1 if status_payment == "approved" else 0
            reference_num = f"{clifor.fk_usuario_id}_CARTAO_MPAG_{datetime.timestamp(datetime.now())}"

            processamento_pedido = ProcessamentoPedido(
                fk_empresa_id=pedido.fk_empresa_id,
                fk_clifor_id=pedido.fk_clifor_id,
                fk_forma_pagamento_id=pedido.fk_forma_pagamento_id,
                data_processamento=get_current_time(),
                valor=pedido.valor_total_pedido,
                status_processamento=status_processamento,
                id_transacao_gateway=reference_num,
                transaction_id=transaction_id,
                data_criacao=get_current_time(),
                usuario_criacao=clifor.fk_usuario_id,
            )

            db.session.add(processamento_pedido)
            db.session.commit()

            return {}, 200

    def __get_processamento_pedido(self, data_id):
        return ProcessamentoPedido.query.filter_by(
            transaction_id=data_id
        ).first()

    def __get_pedido(self, data_id):
        return Pedido.query.filter_by(order_id=data_id).first()

    def __update_processamento_pedido(self, processamento_pedido, response):
        if (
            response.get("status") == "cancelled"
            and response.get("status_detail") == "expired"
        ):
            processamento_pedido.status_processamento = 2
            processamento_pedido.data_processamento = get_current_time()
            processamento_pedido.id_pagamento = response.get(
                "transaction_details", {}
            ).get("transaction_id")
        elif response.get("status") == "approved":
            processamento_pedido.status_processamento = 1
            processamento_pedido.data_processamento = get_current_time()
            processamento_pedido.id_pagamento = response.get(
                "transaction_details", {}
            ).get("transaction_id")

        db.session.commit()
