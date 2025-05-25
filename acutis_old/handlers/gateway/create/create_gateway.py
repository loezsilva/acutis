from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import current_user
from exceptions.error_types.http_conflict import ConflictError
from exceptions.errors_handler import errors_handler
from models.gateway_pagamento import GatewayPagamento


class CreateGateway:
    def __init__(self, conn: SQLAlchemy) -> None:
        self.__conn = conn
        try:
            self.__http_request = request.json

            self.__descricao = self.__http_request["descricao"]
            self.__status = self.__http_request["status"]
            self.__merchant_id = self.__http_request.get("merchant_id")
            self.__merchant_key = self.__http_request.get("merchant_key")

        except KeyError as e:
            errors_handler(e, save_logs=True)

    def execute(self):
        self.__verify_name_gateway()
        self.__insert_new_gateway()
        return self.__format_response()
    
    def __verify_name_gateway(self) -> None:
        gateways = (
            self.__conn.session.query(GatewayPagamento)
            .filter(GatewayPagamento.descricao == self.__descricao)
            .first()
        )
        if gateways is not None:
            raise ConflictError("Nome de gateway não disponível")

    def __insert_new_gateway(self) -> tuple:
        try:
            new_gateway = GatewayPagamento(
                fk_empresa_id=1,
                descricao=self.__descricao,
                status=self.__status,
                merchant_id=self.__merchant_id,
                merchant_key=self.__merchant_key,
                usuario_criacao=current_user["id"]
            )
            
            self.__conn.session.add(new_gateway)
            self.__conn.session.commit()
            
        except Exception as e:
            self.__conn.session.rollback()
            errors_handler(e, save_logs=True)
            
    def __format_response(self):
        return {"msg": "Gateway cadastrado com sucesso"}, 201