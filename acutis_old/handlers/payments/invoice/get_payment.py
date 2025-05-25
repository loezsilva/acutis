import logging

from exceptions.exception_mercado_pago import MercadoPagoException
from services.itau_api import ItauAPI
from services.mercado_pago_api import MercadoPago
from builder import translator


class GetInvoicePayment:
    def __init__(
        self, transaction_id: int, fk_gateway_pagamento_id: int
    ) -> None:
        self.__transaction_id = transaction_id
        self.__fk_gateway_pagamento_id = fk_gateway_pagamento_id

    def execute(self):
        METHODS_MAP = {
            1: self.__itau_invoice_payment,
            2: self.__mercado_pago_invoice_payment,
        }

        resend_payment = METHODS_MAP[self.__fk_gateway_pagamento_id]

        return resend_payment()

    def __itau_invoice_payment(self):
        try:
            itau_api = ItauAPI("boleto")

            data, status_code = itau_api.get(
                path=f"/boletos?id_beneficiario=382700998646&nosso_numero={self.__transaction_id}"
            )

            if status_code not in [200, 201, 204]:
                return {"error": "Ocorreu um erro ao buscar o pagamento."}, 500

            if len(data["data"]) < 1:
                return {
                    "error": "O boleto ainda está sendo gerado. Tente novamente mais tarde!"
                }, 500

            response = data["data"][0]
            response["msg"] = "Boleto gerado com sucesso."

            return response, 200

        except Exception as err:
            logging.error(err)
            return {"error": "Ocorreu um erro ao gerar o pagamento."}, 500

    def __mercado_pago_invoice_payment(self):
        try:
            mp = MercadoPago()

            mp_response = mp.get_payment(self.__transaction_id)

            if mp_response.get("status") != "pending":
                return {"error": "Este pagamento não está mais ativo."}, 400

            return mp_response, 200

        except MercadoPagoException as exception:
            error = translator.translate(exception.error_message)
            return {
                "error": str(error),
            }, exception.status_code

        except Exception as err:
            logging.error(err)
            return {"error": "Ocorreu um erro ao gerar o pagamento."}, 500
