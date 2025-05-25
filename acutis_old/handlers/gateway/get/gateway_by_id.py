from exceptions.error_types.http_not_found import NotFoundError
from models.gateway_pagamento import GatewayPagamento

class GetGatewayByID:
    def __init__(self, gateway_id: int, conn) -> None:
        self.__gateway_id = gateway_id
        self.__conn = conn

    def execute(self):
        gateway: GatewayPagamento = self.__get_gateway()
        return self.__response_format(gateway)

    def __get_gateway(self):
        payment_gateway = self.__conn.session.get(GatewayPagamento, self.__gateway_id)
        if payment_gateway is None:
            raise NotFoundError("Gateway de pagamento não encontrado")

        return payment_gateway

    def __response_format(self, gateway: GatewayPagamento) -> tuple:
        response  = {
            "descricao": gateway.descricao,
            "id": gateway.id
        }
        
        return response, 200