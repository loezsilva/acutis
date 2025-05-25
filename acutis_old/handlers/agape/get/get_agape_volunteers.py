from http import HTTPStatus
import math
from flask import request
from models.schemas.agape.get.get_agape_volunteers import (
    AgapeVoluntarySchema,
    GetAgapeVolunteersResponse,
)
from models.schemas.default import PaginationQuery
from models.usuario import Usuario
from repositories.agape_repository import AgapeRepository


class GetAgapeVolunteers:
    def __init__(self, repository: AgapeRepository):
        self.__repository = repository

    def execute(self):
        filtros = PaginationQuery.parse_obj(request.args)
        voluntarios, total = self.__repository.get_all_agape_volunteers(
            filtros
        )
        response = self.__prepare_response(voluntarios, total, filtros)

        return response, HTTPStatus.OK

    def __prepare_response(
        self, voluntarios: list[Usuario], total: int, filtros: PaginationQuery
    ) -> dict:
        response = GetAgapeVolunteersResponse(
            total=total,
            page=filtros.page,
            pages=math.ceil(total / filtros.per_page),
            voluntarios=[
                AgapeVoluntarySchema.from_orm(voluntario).dict()
                for voluntario in voluntarios
            ],
        ).dict()

        return response
