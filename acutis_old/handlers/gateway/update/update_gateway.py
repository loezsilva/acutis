from flask import request
from flask_jwt_extended import current_user
from flask_sqlalchemy import SQLAlchemy
from exceptions.error_types.http_not_found import NotFoundError
from exceptions.errors_handler import errors_handler
from handlers import gateway
from models.gateway_pagamento import GatewayPagamento
from utils.functions import get_current_time

class UpdateGateway:
    def __init__(self, conn: SQLAlchemy, gateway_id: int) -> None:
        self.__conn = conn
        self.__gateway_id = gateway_id
        try:
            self.__http_request = request.json

            self.__descricao = self.__http_request["descricao"]
            self.__status = self.__http_request["status"]
            self.__merchant_id = self.__http_request.get("merchant_id")
            self.__merchant_key = self.__http_request.get("merchant_key")

        except KeyError as e:
            errors_handler(e, save_logs=True)
    
    def execute(self):
        gateway = self.__get_gateway()
        self.__apply_update(gateway)
        return self.__format_response()
        
    def __get_gateway(self):
        gateway = self.__conn.session.query(GatewayPagamento).filter(GatewayPagamento.id == self.__gateway_id).first()
        
        if gateway is None:
            raise NotFoundError("Gateway não encontrado")
        
        return gateway
    
    def __apply_update(self, payment_gateway: GatewayPagamento):
        try:
            payment_gateway.descricao = self.__descricao
            payment_gateway.status = self.__status
            payment_gateway.merchant_id = self.__merchant_id
            payment_gateway.merchant_key = self.__merchant_key
            payment_gateway.data_alteracao = get_current_time()
            payment_gateway.usuario_alteracao = current_user["id"]
            
            self.__conn.session.commit()
            
        except Exception as e:
            self.__conn.session.rollback()
            errors_handler(e, save_logs=True)
            
    def __format_response(self) -> tuple:
        return {"msg": "Gatewaty atualizado com sucesso"}, 200