from http import HTTPStatus
from typing import Dict

from exceptions.error_types.http_not_found import NotFoundError
from models.endereco import Endereco
from models.schemas.agape.get.get_family_address_by_id import (
    GetFamilyAddressByIdResponse,
)
from repositories.interfaces.agape_repository_interface import (
    AgapeRepositoryInterface,
)


class GetFamilyAddressById:
    def __init__(self, repository: AgapeRepositoryInterface):
        self.__repository = repository

    def execute(self, fk_familia_agape_id: int):
        address = self.__get_family_address_data(fk_familia_agape_id)
        response = self.__prepare_response(address)

        return response, HTTPStatus.OK

    def __get_family_address_data(self, fk_familia_agape_id: int) -> Endereco:
        family = self.__repository.get_agape_family_by_id(fk_familia_agape_id)
        if family is None or family.deleted_at is not None:
            raise NotFoundError("Familia não encontrada.")

        address = self.__repository.get_agape_family_address_by_id(
            family.fk_endereco_id
        )
        return address

    def __prepare_response(self, address: Endereco) -> Dict:
        response = GetFamilyAddressByIdResponse.from_orm(address).dict()
        return response
