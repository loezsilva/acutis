import logging
from uuid import uuid4
from flask_jwt_extended import current_user
import requests
from config import MAXIPAGO_URL_XML
from exceptions.exception_mercado_pago import MercadoPagoException
from builder import db, translator
from models.campanha import Campanha
from models.gateway_pagamento import GatewayPagamento
from services.mercado_pago_api import MercadoPago
from utils.logs_access import log_access
import xmltodict


class ReverseCreditCardPayment:
    def __init__(self, pedido) -> None:
        self.__pedido = pedido

    def execute(self):
        METHODS_MAP = {
            1: self.__maxipago_reverse_payment,
            2: self.__mercado_pago_reverse_payment,
        }

        payment_gateway = METHODS_MAP[self.__pedido.fk_gateway_pagamento_id]
        return payment_gateway()

    def __maxipago_reverse_payment(self):
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

            if (
                gateway_pagamento := GatewayPagamento.query.filter_by(
                    fk_empresa_id=campanha.fk_empresa_id
                ).first()
            ) is None:
                response = {"error": "Gateway de pagamento não encontrado."}
                log_access(
                    response,
                    current_user["id"],
                    current_user["nome"],
                    current_user["fk_perfil_id"],
                )
                return response, 404

            url = MAXIPAGO_URL_XML
            headers = {"Content-Type": "text/xml"}

            reference_num = uuid4().hex

            transaction_request = f"""
                <transaction-request>
                    <version>3.1.1.15</version>
                    <verification>
                        <merchantId>{gateway_pagamento.merchant_id}</merchantId>
                        <merchantKey>{gateway_pagamento.merchant_key}</merchantKey>
                    </verification>
                    <order>
                        <return>
                            <orderID>{self.__pedido.order_id}</orderID>
                            <referenceNum>{reference_num}</referenceNum>
                            <payment>
                                <chargeTotal>{self.__pedido.valor_total_pedido}</chargeTotal>
                            </payment>
                        </return>
                    </order>
                </transaction-request>
            """

            response = requests.post(
                url, data=transaction_request, headers=headers
            )

            if not str(response.status_code).startswith("2"):
                raise Exception(response)

            response = (xmltodict.parse(response.text)).get(
                "transaction-response"
            )

            if response.get("responseCode") == "1024":
                message = response.get("errorMessage")
                message = translator.translate(message)
                return {"error": message}, 400

            self.__pedido.status_pedido = 2  # Cancelada

            db.session.commit()

            log_access(
                str({"msg": "O estorno do valor foi efetuado com sucesso."}),
                current_user["id"],
                current_user["nome"],
                current_user["fk_perfil_id"],
                200,
            )

            return {"msg": "O estorno do valor foi efetuado com sucesso."}, 200

        except Exception as err:
            logging.error(f"{str(type(err))} - {str(err)}")
            return {
                "error": "Ocorreu um erro ao estornar o pagamento do usuário."
            }, 500

    def __mercado_pago_reverse_payment(self):
        try:
            mp = MercadoPago()

            mp_response = mp.refund_payment(payment_id=self.__pedido.order_id)

            if mp_response.get("status") != "approved":
                return {
                    "error": "Ocorreu um erro ao estornar o pagamento. Tente novamente mais tarde!"
                }

            self.__pedido.status_pedido = 2
            db.session.commit()

            return {"msg": "O estorno do valor foi efetuado com sucesso."}, 200

        except MercadoPagoException as mp_exception:
            error = translator.translate(mp_exception.error_message)
            return {"error": error}, mp_exception.status_code

        except Exception as err:
            db.session.rollback()
            logging.error(f"{str(type(err))} - {str(err)}")
            return {
                "error": "Ocorreu um erro ao estornar o pagamento do usuário."
            }, 500
