from http import HTTPStatus
import math

from flask import request
from models.agape.familia_agape import FamiliaAgape
from models.schemas.agape.get.get_all_agape_families import (
    AgapeFamilySchema,
    GetAllAgapeFamiliesResponse,
)
from models.schemas.default import PaginationQuery
from repositories.interfaces.agape_repository_interface import (
    AgapeRepositoryInterface,
)
from services.file_service import FileService


class GetAllAgapeFamilies:
    def __init__(
        self, repository: AgapeRepositoryInterface, file_service: FileService
    ) -> None:
        self.__repository = repository
        self.__file_service = file_service

    def execute(self):
        filtros = PaginationQuery.parse_obj(request.args)
        families, total = self.__get_families(filtros)
        response = self.__prepare_response(families, total, filtros)

        return response, HTTPStatus.OK

    def __get_families(
        self, filtros: PaginationQuery
    ) -> tuple[FamiliaAgape, int]:
        families_query = self.__repository.get_all_families()
        families, total = self.__repository.paginate_query(
            query=families_query, page=filtros.page, per_page=filtros.per_page
        )

        return families, total

    def __prepare_response(
        self,
        families: list[FamiliaAgape],
        total: int,
        filtros: PaginationQuery,
    ) -> dict:
        familias = []
        for db_familia in families:
            fotos_familia = (
                self.__repository.buscar_fotos_por_familia_agape_id(
                    db_familia.id
                )
            )

            familia = AgapeFamilySchema(
                id=db_familia.id,
                familia=db_familia.familia,
                membros=db_familia.membros,
                renda=db_familia.renda,
                cadastrado_em=db_familia.cadastrado_em,
                ultimo_recebimento=db_familia.ultimo_recebimento,
                comprovante_residencia=(
                    self.__file_service.get_public_url(db_familia.comprovante_residencia)
                    if db_familia.comprovante_residencia
                    else None
                ),
                observacao=db_familia.observacao,
                recebimentos=db_familia.recebimentos,
                fk_endereco_id=db_familia.fk_endereco_id,
                cadastrada_por=db_familia.cadastrada_por,
                fotos_familia=[
                    self.__file_service.get_public_url(
                        foto_familia.foto
                    ) 
                    for foto_familia in fotos_familia
                ]
            ).dict()
            familias.append(familia)

        response = GetAllAgapeFamiliesResponse(
            page=filtros.page,
            pages=math.ceil(total / filtros.per_page),
            total=total,
            familias=familias,
        ).dict()

        return response
