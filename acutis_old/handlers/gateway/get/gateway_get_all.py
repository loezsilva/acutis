from flask import request
from flask_sqlalchemy import SQLAlchemy
from exceptions.error_types.http_not_found import NotFoundError
from models.gateway_pagamento import GatewayPagamento


class  GatewayGetAll:
    def __init__(self) -> None:
        self.__http_args = request.args
        self.__page = self.__http_args.get("page", 1, type=int)
        self.__per_page = self.__http_args.get("per_page", 10, type=int)
        
    def execute(self):
        
        gateways = self.__query_get_all()
        return self.__format_response(gateways)
    
    def __query_get_all(self) -> GatewayPagamento:
        gateways = GatewayPagamento.query.order_by(GatewayPagamento.data_criacao.desc())
        
        if gateways is None:
            raise NotFoundError("Nenhum gateway de pagamento")
        
        paginate = gateways.paginate(page=self.__page, per_page=self.__per_page)
        return paginate
    
    def __format_response(self, data: tuple) -> tuple:
        
        res  = [
            {
                "descricao": data.descricao,
                "id":  data.id
            } for data in data.items
        ]
        
        return res, 200
    