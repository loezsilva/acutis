from http import HTTPStatus
from typing import Dict, List, Tuple
from flask import request
from flask_jwt_extended import current_user
from models.schemas.agape.get.get_all_agape_actions_instances import (
    AgapeActionInstanceSchema,
    GetAllAgapeActionsInstancesQuery,
    GetAllAgapeActionsInstancesResponse,
)
from repositories.interfaces.agape_repository_interface import (
    AgapeRepositoryInterface,
)


class GetAllAgapeActionsInstances:
    def __init__(self, repository: AgapeRepositoryInterface):
        self.__repository = repository

    def execute(self):
        perfil = current_user["nome_perfil"]
        filtros = GetAllAgapeActionsInstancesQuery.parse_obj(request.args)
        instancias, total = self.__get_all_agape_actions_instances(
            filtros, perfil
        )
        response = self.__prepare_response(instancias, total, filtros.page)

        return response, HTTPStatus.OK

    def __get_all_agape_actions_instances(
        self, filtros: GetAllAgapeActionsInstancesQuery, perfil: str
    ) -> Tuple[List[AgapeActionInstanceSchema], int]:
        instancias_query = self.__repository.get_all_agape_action_instances(
            filtros, perfil
        )
        instancias, total = self.__repository.paginate_query(
            instancias_query, filtros.page, filtros.per_page
        )
        return instancias, total

    def __prepare_response(
        self,
        instancias: List[AgapeActionInstanceSchema],
        total: int,
        page: int,
    ) -> Dict:
        response = GetAllAgapeActionsInstancesResponse(
            total=total,
            page=page,
            ciclos=[
                AgapeActionInstanceSchema.from_orm(instancia).dict()
                for instancia in instancias
            ],
        ).dict()

        return response
