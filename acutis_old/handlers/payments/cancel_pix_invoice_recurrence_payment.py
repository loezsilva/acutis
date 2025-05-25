import logging
from flask_jwt_extended import current_user
from utils.functions import get_current_time
from utils.logs_access import log_access
from builder import db


class CancelPixInvoiceRecurrencePayment:

    def __init__(self, pedido) -> None:
        self.__pedido = pedido

    def execute(self):
        return self.__cancel_recurrence_payment()

    def __cancel_recurrence_payment(self):
        try:
            if not self.__pedido.recorrencia_ativa:
                response = {
                    "error": "Este pedido não possui recorrência ativa."
                }, 400
                log_access(
                    response,
                    current_user["id"],
                    current_user["nome"],
                    current_user["fk_perfil_id"],
                )
                return response

            self.__pedido.recorrencia_ativa = False
            self.__pedido.status_pedido = 2
            self.__pedido.cancelada_em = get_current_time()
            self.__pedido.cancelada_por = current_user["id"]

            db.session.commit()

            response = {"msg": "Recorrência cancelada com sucesso."}, 200
            log_access(
                response,
                current_user["id"],
                current_user["nome"],
                current_user["fk_perfil_id"],
            )
            return response

        except Exception as exception:
            db.session.rollback()
            logging.error(str(exception))
            response = {
                "error": "Ocorreu um erro ao cancelar a recorrência",
            }
            log_access(
                response,
                current_user["id"],
                current_user["nome"],
                current_user["fk_perfil_id"],
            )
            return response, 500
