from http import HTTPStatus
from typing import Dict, List, Tuple

from flask import request
from exceptions.error_types.http_not_found import NotFoundError
from models.schemas.agape.get.get_all_donations_receipts import (
    DonationReceiptSchema,
    GetAllDonationsReceiptsResponse,
)
from models.schemas.default import PaginationQuery
from repositories.interfaces.agape_repository_interface import (
    AgapeRepositoryInterface,
)
from services.file_service import FileService


class GetAllDonationsReceipts:
    def __init__(
        self, repository: AgapeRepositoryInterface, file_service: FileService
    ) -> None:
        self.__repository = repository
        self.__file_service = file_service

    def execute(self, fk_familia_agape_id: int):
        filtros = PaginationQuery.parse_obj(request.args)
        self.__check_if_family_exists(fk_familia_agape_id)
        doacoes, total = self.__get_all_receipts(fk_familia_agape_id, filtros)
        response = self.__prepare_response(doacoes, total, filtros.page)

        return response, HTTPStatus.OK

    def __check_if_family_exists(self, fk_familia_agape_id: int):
        family = self.__repository.get_agape_family_by_id(fk_familia_agape_id)
        if family is None or family.deleted_at is not None:
            raise NotFoundError("Familia não encontrada.")

    def __get_all_receipts(
        self, fk_familia_agape_id: int, filtros: PaginationQuery
    ) -> Tuple[List[DonationReceiptSchema], int]:
        doacoes_query = self.__repository.get_all_donations_receipts(
            fk_familia_agape_id
        )
        doacoes, total = self.__repository.paginate_query(
            doacoes_query, filtros.page, filtros.per_page
        )

        return doacoes, total

    def __prepare_response(
        self, doacoes: List[DonationReceiptSchema], total: int, page: int
    ) -> Dict:
        response = GetAllDonationsReceiptsResponse(
            total=total,
            page=page,
            doacoes_recebidas=[
                DonationReceiptSchema(
                    nome_acao=doacao.nome_acao,
                    fk_doacao_agape_id=doacao.fk_doacao_agape_id,
                    fk_instancia_acao_agape_id=doacao.fk_instancia_acao_agape_id,
                    dia_horario=doacao.dia_horario,
                    recibos=[
                        self.__file_service.get_public_url(recibo)
                        for recibo in doacao.recibos.split(",")
                        if recibo
                    ],
                ).dict()
                for doacao in doacoes
            ],
        ).dict()

        return response
