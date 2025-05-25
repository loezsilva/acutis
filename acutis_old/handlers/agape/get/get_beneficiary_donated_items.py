from http import HTTPStatus
from typing import Dict, List
from models.schemas.agape.get.get_beneficiary_donated_items import (
    DonatedItemSchema,
    GetBeneficiaryDonatedItemsResponse,
)
from repositories.interfaces.agape_repository_interface import (
    AgapeRepositoryInterface,
)


class GetBeneficiaryDonatedItems:
    def __init__(self, repository: AgapeRepositoryInterface) -> None:
        self.__repository = repository

    def execute(self, fk_doacao_agape_id: int):
        itens = self.__get_donated_items(fk_doacao_agape_id)
        response = self.__prepare_response(itens)
        return response, HTTPStatus.OK

    def __get_donated_items(
        self, fk_doacao_agape_id: int
    ) -> List[DonatedItemSchema]:
        itens = self.__repository.get_beneficiary_donated_items(
            fk_doacao_agape_id
        )
        return itens

    def __prepare_response(self, itens: List[DonatedItemSchema]) -> Dict:
        response = GetBeneficiaryDonatedItemsResponse(
            itens_doados=[
                DonatedItemSchema.from_orm(item).dict() for item in itens
            ]
        ).dict()
        return response
