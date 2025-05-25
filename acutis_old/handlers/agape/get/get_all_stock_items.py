from http import HTTPStatus
from typing import Dict, List

from models.agape.estoque_agape import EstoqueAgape
from models.schemas.agape.get.get_all_stock_items import (
    GetAllStockItemsResponse,
    StockItemSchema,
)


class GetAllStockItems:
    def execute(self):
        estoques = self.__get_stock_items()
        response = self.__prepare_response(estoques)
        return response, HTTPStatus.OK

    def __get_stock_items(self) -> List[EstoqueAgape]:
        estoques = EstoqueAgape.query.all()
        return estoques

    def __prepare_response(self, estoques: List[EstoqueAgape]) -> Dict:
        response = GetAllStockItemsResponse(
            estoques=[
                StockItemSchema.from_orm(estoque).dict()
                for estoque in estoques
            ]
        ).dict()

        return response
