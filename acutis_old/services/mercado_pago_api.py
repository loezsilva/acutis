from config import MERCADO_PAGO_ACCESS_TOKEN
import uuid
import mercadopago
from mercadopago.core import MPBase
from mercadopago.http import HttpClient
from mercadopago.config import RequestOptions
from exceptions.exception_mercado_pago import MercadoPagoException


class MercadoPago(MPBase):
    def __init__(self):
        self.__req_options = RequestOptions()
        self.__req_options.custom_headers = {
            'x-idempotency-key': str(uuid.uuid4())
        }

        http_client = HttpClient()

        super().__init__(self.__req_options, http_client)
        self.__sdk = mercadopago.SDK(MERCADO_PAGO_ACCESS_TOKEN)

    def __execute_request(self, request_func, *args, **kwargs):
        request_options = kwargs.get('request_options', self.__req_options)
        additional_headers = kwargs.get('additional_headers')
        if additional_headers:
            request_options.custom_headers.update(additional_headers)

        response = request_func(*args, request_options)

        if response["status"] not in [200, 201, 204]:
            raise MercadoPagoException(
                response['response']['message'], response["status"])
        return response['response']

    def create_card_token(self, card_data):
        return self.__execute_request(self.__sdk.card_token().create, card_data)

    def create_payment(self, payment_data, device_id=None):
        additional_headers = {
            'X-meli-session-id': device_id} if device_id else None

        return self.__execute_request(self.__sdk.payment().create, payment_data, additional_headers=additional_headers)

    def create_recurrence_payment(self, payment_data, device_id=None):
        additional_headers = {
            'X-meli-session-id': device_id} if device_id else None
        return self.__execute_request(self.__sdk.preapproval().create, payment_data, additional_headers=additional_headers)

    def get_payment_methods(self):
        return self.__execute_request(self.__sdk.payment_methods().list_all())

    def get_payment(self, payment_id):
        return self.__execute_request(self.__sdk.payment().get, payment_id)

    def search_payments(self, filters: dict):
        return self.__execute_request(self.__sdk.payment().search, filters)

    def get_authorized_payment(self, id):
        response = self._get(
            uri="/authorized_payments/" + str(id),
            request_options=self.__req_options)

        if response["status"] not in [200, 201, 204]:
            raise MercadoPagoException(
                response['response']['message'], response["status"])
        return response['response']

    def get_preapproval(self, preapproval_id):
        return self.__execute_request(self.__sdk.preapproval().get, preapproval_id)

    def update_payment(self, payment_id, payment_object):
        return self.__execute_request(self.__sdk.payment().update, payment_id, payment_object, request_options=self.__req_options)

    def refund_payment(self, payment_id, refund_object={}):
        return self.__execute_request(self.__sdk.refund().create, payment_id, refund_object)

    def update_recurrence_payment(self, preapproval_id, preapproval_object):
        return self.__execute_request(self.__sdk.preapproval().update, f"/{preapproval_id}", preapproval_object, request_options=self.__req_options)
