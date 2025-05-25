from http import HTTPStatus
from typing import Dict, List, Tuple
from flask import request

from models.agape.doacao_agape import DoacaoAgape
from models.schemas.agape.get.get_beneficiaries_by_agape_action_id import (
    BeneficiariesSchema,
    GetBeneficiariesByAgapeActionIdQuery,
    GetBeneficiariesByAgapeActionIdResponse,
)
from repositories.interfaces.agape_repository_interface import (
    AgapeRepositoryInterface,
)
from services.file_service import FileService


class GetBeneficiariesByAgapeActionInstanceId:
    def __init__(
        self, repository: AgapeRepositoryInterface, file_service: FileService
    ) -> None:
        self.__repository = repository
        self.__file_service = file_service

    def execute(self, fk_instancia_acao_agape_id: int):
        filtros = GetBeneficiariesByAgapeActionIdQuery.parse_obj(request.args)
        beneficiarios, total = self.__get_beneficiaries(
            fk_instancia_acao_agape_id, filtros
        )
        response = self.__prepare_response(beneficiarios, total, filtros.page)

        return response, HTTPStatus.OK

    def __get_beneficiaries(
        self,
        fk_instancia_acao_agape_id: int,
        filtros: GetBeneficiariesByAgapeActionIdQuery,
    ) -> Tuple[List[BeneficiariesSchema], int]:
        beneficiarios_query = (
            self.__repository.get_beneficiaries_by_agape_action_instance_id(
                fk_instancia_acao_agape_id, filtros
            )
        )

        beneficiarios, total = self.__repository.paginate_query(
            beneficiarios_query, filtros.page, filtros.per_page
        )
        return beneficiarios, total

    def __prepare_response(
        self, beneficiarios: list[DoacaoAgape], total: int, page: int
    ) -> Dict:
        response = GetBeneficiariesByAgapeActionIdResponse(
            page=page,
            total=total,
            beneficiarios=[
                BeneficiariesSchema(
                    fk_doacao_agape_id=beneficiario.fk_doacao_agape_id,
                    nome_familia=beneficiario.nome_familia,
                    data_hora_doacao=beneficiario.data_hora_doacao,
                    recibos=[
                        self.__file_service.get_public_url(recibo)
                        for recibo in beneficiario.recibos.split(",")
                        if recibo
                    ],
                ).dict()
                for beneficiario in beneficiarios
            ],
        ).dict()

        return response
