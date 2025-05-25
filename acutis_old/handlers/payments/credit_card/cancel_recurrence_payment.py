import logging
from flask_jwt_extended import current_user
import requests
import xmltodict

from config import MAXIPAGO_URL_API
from exceptions.exception_mercado_pago import MercadoPagoException
from models.campanha import Campanha
from models.gateway_pagamento import GatewayPagamento
from builder import db, translator
from services.mercado_pago_api import MercadoPago
from utils.functions import get_current_time
from utils.logs_access import log_access


class CancelCreditCardRecurrencePayment:
    def __init__(self, pedido) -> None:
        self.__pedido = pedido

    def execute(self):
        METHODS_MAP = {
            1: self.__maxi_pago_cancel_recurrence_payment,
            2: self.__mercado_pago_cancel_recurrence_payment,
        }

        payment_gateway = METHODS_MAP[self.__pedido.fk_gateway_pagamento_id]
        return payment_gateway()

    def __maxi_pago_cancel_recurrence_payment(self):
        try:
            if (
                campanha := db.session.get(
                    Campanha, self.__pedido.fk_campanha_id
                )
            ) is None:
                response = {"error": "Campanha não encontrada."}
                log_access(
                    response,
                    current_user["id"],
                    current_user["nome"],
                    current_user["fk_perfil_id"],
                )
                return response, 404

            gateway_pagamento = GatewayPagamento.query.filter_by(
                fk_empresa_id=campanha.fk_empresa_id
            ).first()
            if not gateway_pagamento:
                response = {"error": "Gateway de pagamento não encontrado."}
                log_access(
                    response,
                    current_user["id"],
                    current_user["nome"],
                    current_user["fk_perfil_id"],
                )
                return response, 404

            url = MAXIPAGO_URL_API
            headers = {"Content-Type": "text/xml"}

            credit_card_cancel_recurrence_xml = f"""
                <api-request>
                    <verification>
                        <merchantId>{gateway_pagamento.merchant_id}</merchantId>
                        <merchantKey>{gateway_pagamento.merchant_key}</merchantKey>
                    </verification>
                    <command>cancel-recurring</command>
                    <request>
                        <orderID>{self.__pedido.order_id}</orderID>
                    </request>
                </api-request>
            """

            response = requests.post(
                url, data=credit_card_cancel_recurrence_xml, headers=headers
            )

            if not str(response.status_code).startswith("2"):
                logging.error(
                    "Error %s: %s" % (response.status_code, response.reason)
                )
                response = {
                    "error": "Ocorreu uma falha ao cancelar a recorrência."
                }
                log_access(
                    response,
                    current_user["id"],
                    current_user["nome"],
                    current_user["fk_perfil_id"],
                )
                return response, 500

            response = xmltodict.parse(response.text)

            try:
                transaction = response["api-response"]
                error_code = int(transaction["errorCode"])
                error_message = transaction["errorMessage"]

                if error_code != 0:
                    if (
                        "CANCELLED" in error_message
                        or "equals to COMPLETE" in error_message
                    ):
                        if not self.__pedido.recorrencia_ativa:
                            response = {
                                "error": "A recorrência de pagamento já foi cancelada."
                            }
                            log_access(
                                response,
                                current_user["id"],
                                current_user["nome"],
                                current_user["fk_perfil_id"],
                            )
                            return response, 409
                        self.__pedido.recorrencia_ativa = False
                        self.__pedido.status_pedido = 2
                        self.__pedido.cancelada_em = get_current_time()
                        self.__pedido.cancelada_por = current_user["id"]
                        
                        db.session.commit()
                        return {
                            "msg": "A recorrência de pagamento foi cancelada com sucesso."
                        }, 200

                    elif "Invalid" in error_message:
                        response = {
                            "error": "A recorrência de pagamento não foi encontrada."
                        }
                        log_access(
                            response,
                            current_user["id"],
                            current_user["nome"],
                            current_user["fk_perfil_id"],
                        )
                        return response, 404
                    else:
                        response = {
                            "error": "Ocorreu uma falha ao cancelar a recorrência.",
                            "error_message": transaction["errorMessage"],
                        }
                        log_access(
                            response,
                            current_user["id"],
                            current_user["nome"],
                            current_user["fk_perfil_id"],
                        )
                        return response, 400
                self.__pedido.recorrencia_ativa = False
                self.__pedido.status_pedido = 2
                self.__pedido.cancelada_em = get_current_time()
                db.session.commit()

                response = {
                    "msg": "A recorrência de pagamento foi cancelada com sucesso."
                }
                log_access(
                    response,
                    current_user["id"],
                    current_user["nome"],
                    current_user["fk_perfil_id"],
                )
                return response, 200

            except KeyError as err:
                logging.error(response)
                response = {
                    "error": "Ocorreu uma falha ao cancelar a recorrência."
                }
                log_access(
                    response,
                    current_user["id"],
                    current_user["nome"],
                    current_user["fk_perfil_id"],
                )
                return response, 500

        except Exception as err:
            db.session.rollback()
            logging.error(f"{type(err)} - {err}")
            response = {"error": str(err)}
            log_access(
                response,
                current_user["id"],
                current_user["nome"],
                current_user["fk_perfil_id"],
            )
            return response, 500

    def __mercado_pago_cancel_recurrence_payment(self):
        try:
            payment_data = {"status": "cancelled"}

            mp = MercadoPago()
            mp_response = mp.update_recurrence_payment(
                self.__pedido.order_id, payment_data
            )
            if mp_response.get("status") != "cancelled":
                return {
                    "error": "Ocorreu um erro ao cancelar a recorrência. Tente novamente mais tarde!"
                }

            self.__pedido.recorrencia_ativa = False
            self.__pedido.status_pedido = 2
            self.__pedido.cancelada_em = get_current_time()
            db.session.commit()

            return {"msg": "Recorrência cancelada com sucesso."}, 200

        except MercadoPagoException as mp_exception:
            error = translator.translate(mp_exception.error_message)
            return {"error": error}, mp_exception.status_code

        except Exception as err:
            logging.error(err)
            db.session.rollback()
            response = {
                "error": "Ocorreu um erro ao cancelar a recorrência. Tente novamente mais tarde!"
            }
            log_access(
                response,
                current_user["id"],
                current_user["nome"],
                current_user["fk_perfil_id"],
            )
            return response, 500
