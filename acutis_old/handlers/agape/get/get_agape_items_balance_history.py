from http import HTTPStatus
from typing import Dict, List, Tuple
from flask import request
from models.schemas.agape.get.get_agape_items_balance_history import (
    GetAgapeItemsBalanceHistoryQuery,
    GetAgapeItemsBalanceHistoryResponse,
    ItemBalanceHistorySchema,
)
from repositories.interfaces.agape_repository_interface import (
    AgapeRepositoryInterface,
)


class GetAgapeItemsBalanceHistory:
    def __init__(self, repository: AgapeRepositoryInterface) -> None:
        self.__repository = repository

    def execute(self):
        filtros = GetAgapeItemsBalanceHistoryQuery.parse_obj(request.args)
        movimentacoes, total = self.__get_items_balance_history(filtros)
        response = self.__prepare_response(movimentacoes, total, filtros.page)

        return response, HTTPStatus.OK

    def __get_items_balance_history(
        self, filtros: GetAgapeItemsBalanceHistoryQuery
    ) -> Tuple[List[ItemBalanceHistorySchema], int]:
        movimentacoes_query = (
            self.__repository.get_agape_items_balance_history(filtros)
        )
        movimentacoes, total = self.__repository.paginate_query(
            movimentacoes_query, filtros.page, filtros.per_page
        )
        return movimentacoes, total

    def __prepare_response(
        self,
        movimentacoes: List[ItemBalanceHistorySchema],
        total: int,
        page: int,
    ) -> Dict:
        response = GetAgapeItemsBalanceHistoryResponse(
            total=total,
            page=page,
            movimentacoes=[
                ItemBalanceHistorySchema.from_orm(movimentacao).dict()
                for movimentacao in movimentacoes
            ],
        ).dict()
        return response
