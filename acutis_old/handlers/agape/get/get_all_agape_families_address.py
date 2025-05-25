from http import HTTPStatus
from typing import List
from models.schemas.agape.get.get_all_agape_families_address import (
    AgapeFamilyAddress,
    GetAllAgapeFamiliesAddressResponse,
)
from repositories.interfaces.agape_repository_interface import (
    AgapeRepositoryInterface,
)


class GetAllAgapeFamiliesAddress:
    def __init__(self, repository: AgapeRepositoryInterface) -> None:
        self.__repository = repository

    def execute(self):
        enderecos = self.__repository.get_all_agape_families_address()
        response = self.__prepare_response(enderecos)

        return response, HTTPStatus.OK

    def __prepare_response(self, enderecos: List[AgapeFamilyAddress]):
        response = GetAllAgapeFamiliesAddressResponse(
            enderecos=[
                AgapeFamilyAddress.from_orm(endereco).dict()
                for endereco in enderecos
            ]
        ).dict()

        return response
