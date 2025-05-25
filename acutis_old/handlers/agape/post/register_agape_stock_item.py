from http import HTTPStatus
from flask_sqlalchemy import SQLAlchemy
from flask import request as flask_request

from exceptions.error_types.http_conflict import ConflictError
from models.agape.estoque_agape import EstoqueAgape
from models.schemas.agape.post.register_agape_stock_item import (
    RegisterAgapeStockItemRequest,
)
from utils.functions import normalize_text


class RegisterAgapeStockItem:
    def __init__(self, database: SQLAlchemy) -> None:
        self.__database = database

    def execute(self):
        request = RegisterAgapeStockItemRequest.parse_obj(flask_request.json)

        self.__check_if_item_already_exists(request.item)
        self.__register_stock(request)

        return {"msg": "Estoque cadastrado com sucesso."}, HTTPStatus.CREATED

    def __check_if_item_already_exists(self, item: str):
        item_normalizado = normalize_text(item)

        itens_estoque = EstoqueAgape.query.all()
        for item_cadastrado in itens_estoque:
            item_cadastrado_normalizado = normalize_text(item_cadastrado.item)
            if item_cadastrado_normalizado == item_normalizado:
                raise ConflictError(f"Item {item} já cadastrado no estoque.")

    def __register_stock(self, request: RegisterAgapeStockItemRequest):
        estoque = EstoqueAgape(item=request.item, quantidade=0)
        self.__database.session.add(estoque)
        self.__database.session.commit()
