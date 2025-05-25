from http import HTTPStatus
from typing import Dict, List, Tuple

from flask import request


from models.schemas.agape.get.get_all_agape_actions import (
    AgapeActionSchema,
    GetAllAgapeActionsQuery,
    GetAllAgapeActionsResponse,
)
from repositories.interfaces.agape_repository_interface import (
    AgapeRepositoryInterface,
)


class GetAllAgapeActions:
    def __init__(self, repository: AgapeRepositoryInterface) -> None:
        self.__repository = repository

    def execute(self):
        filtros = GetAllAgapeActionsQuery.parse_obj(request.args)
        acoes_agape, total = self.__get_all_agape_actions(filtros)
        response = self.__prepare_response(acoes_agape, total, filtros.page)

        return response, HTTPStatus.OK

    def __get_all_agape_actions(
        self, filtros: GetAllAgapeActionsQuery
    ) -> Tuple[List[AgapeActionSchema], int]:
        acoes_agape_query = self.__repository.get_all_agape_actions(filtros)
        acoes_agape, total = self.__repository.paginate_query(
            acoes_agape_query, filtros.page, filtros.per_page
        )
        return acoes_agape, total

    def __prepare_response(
        self, acoes_agape: List[AgapeActionSchema], total: int, page: int
    ) -> Dict:
        response = GetAllAgapeActionsResponse(
            total=total,
            page=page,
            acoes_agape=[
                AgapeActionSchema.from_orm(acao).dict() for acao in acoes_agape
            ],
        ).dict()

        return response
