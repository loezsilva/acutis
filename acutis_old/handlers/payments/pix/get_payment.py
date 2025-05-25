import logging

from exceptions.exception_mercado_pago import MercadoPagoException
from services.itau_api import ItauAPI
from builder import translator
from services.mercado_pago_api import MercadoPago


class GetPixPayment:
    def __init__(
        self, transaction_id: int, fk_gateway_pagamento_id: int
    ) -> None:
        self.__transaction_id = transaction_id
        self.__fk_gateway_pagamento_id = fk_gateway_pagamento_id

    def execute(self):
        METHODS_MAP = {
            1: self.__itau_pix_payment,
            2: self.__mercado_pago_pix_payment,
        }

        resend_payment = METHODS_MAP[self.__fk_gateway_pagamento_id]

        return resend_payment()

    def __itau_pix_payment(self):
        try:
            itau_api = ItauAPI("pix")

            get_pix_payment, status_code_pix = itau_api.get(
                path=f"/cobv/{self.__transaction_id}"
            )

            if status_code_pix not in [200, 201, 204]:
                return {"error": "Ocorreu um erro ao buscar o pagamento."}, 500

            if get_pix_payment["status"] != "ATIVA":
                return {"error": "Este pagamento não está mais ativo."}, 400

            get_qrcode_payment, status_code_qrcode = itau_api.get(
                path=f"/cobv/{self.__transaction_id}/qrcode"
            )

            if status_code_qrcode not in [200, 201, 204]:
                return {
                    "error": "Ocorreu um erro ao gerar o qrcode de pagamento."
                }, 500

            response = {
                "msg": "Pix gerado com sucesso.",
                "pix_qrcode": get_qrcode_payment.get("emv"),
                "qr_code_base64": get_qrcode_payment.get("imagem_base64"),
            }

            return response, 200

        except Exception as err:
            logging.error(err)
            return {"error": "Ocorreu um erro ao gerar o pagamento."}, 500

    def __mercado_pago_pix_payment(self):
        try:
            mp = MercadoPago()

            mp_response = mp.get_payment(self.__transaction_id)

            if mp_response.get("status") != "pending":
                return {"error": "Este pagamento não está mais ativo."}, 400

            response = {
                "msg": "Pix gerado com sucesso.",
                "pix_qrcode": mp_response.get("point_of_interaction")
                .get("transaction_data")
                .get("qr_code"),
                "qr_code_base64": mp_response.get("point_of_interaction")
                .get("transaction_data")
                .get("qr_code_base64"),
            }

            return response, 200

        except MercadoPagoException as exception:
            error = translator.translate(exception.error_message)
            return {
                "error": str(error),
            }, exception.status_code

        except Exception as err:
            logging.error(err)
            return {"error": "Ocorreu um erro ao gerar o pagamento."}, 500
