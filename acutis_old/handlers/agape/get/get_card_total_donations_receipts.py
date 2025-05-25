from http import HTTPStatus
from typing import Dict
from exceptions.error_types.http_not_found import NotFoundError
from models.schemas.agape.get.get_card_total_donations_receipts import (
    GetCardTotalDonationsReceiptsResponse,
)
from repositories.interfaces.agape_repository_interface import (
    AgapeRepositoryInterface,
)
from repositories.schemas.agape_schemas import GetTotalDonationsReceiptsSchema


class GetCardTotalDonationsReceipts:
    def __init__(self, repository: AgapeRepositoryInterface):
        self.__repository = repository

    def execute(self, fk_familia_agape_id):
        self.__check_if_family_exists(fk_familia_agape_id)
        doacoes = self.__repository.get_total_donations_receipts(
            fk_familia_agape_id
        )
        response = self.__prepare_response(doacoes)

        return response, HTTPStatus.OK

    def __check_if_family_exists(self, fk_familia_agape_id: int):
        family = self.__repository.get_agape_family_by_id(fk_familia_agape_id)
        if family is None or family.deleted_at is not None:
            raise NotFoundError("Familia não encontrada.")

    def __prepare_response(
        self, doacoes: GetTotalDonationsReceiptsSchema
    ) -> Dict:
        response = GetCardTotalDonationsReceiptsResponse(
            total_itens_recebidos=f"{doacoes.total_recebidas} Itens recebidos"
        ).dict()
        return response
