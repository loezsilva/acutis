from http import HTTPStatus
from typing import Dict

from exceptions.error_types.http_not_found import NotFoundError
from models.schemas.agape.get.get_card_agape_family_income import (
    GetCardAgapeFamilyIncomeResponse,
)
from repositories.interfaces.agape_repository_interface import (
    AgapeRepositoryInterface,
)
from repositories.schemas.agape_schemas import (
    GetNumberRegisteredAgapeMembersSchema,
    GetSumAgapeFamiliesIncomeSchema,
)


class GetCardAgapeFamilyIncome:
    def __init__(self, repository: AgapeRepositoryInterface) -> None:
        self.__repository = repository

    def execute(self, fk_familia_agape_id: int):
        self.__check_if_family_exists(fk_familia_agape_id)
        membros_cadastrados = (
            self.__repository.get_number_registered_agape_families_members(
                fk_familia_agape_id
            )
        )
        renda_familiar = self.__repository.get_sum_agape_families_income(
            fk_familia_agape_id
        )
        response = self.__prepare_response(membros_cadastrados, renda_familiar)

        return response, HTTPStatus.OK

    def __check_if_family_exists(self, fk_familia_agape_id: int):
        family = self.__repository.get_agape_family_by_id(fk_familia_agape_id)
        if family is None or family.deleted_at is not None:
            raise NotFoundError("Familia não encontrada.")

    def __prepare_response(
        self,
        membros_cadastrados: GetNumberRegisteredAgapeMembersSchema,
        renda_familiar: GetSumAgapeFamiliesIncomeSchema,
    ) -> Dict:
        salario_minimo = 1518
        renda_per_capta = (
            (renda_familiar.total / membros_cadastrados.quantidade)
            / salario_minimo
            if renda_familiar.total > 0
            else 0
        )
        renda_total = (
            renda_familiar.total / salario_minimo
            if renda_familiar.total > 0
            else 0
        )
        response = GetCardAgapeFamilyIncomeResponse(
            renda_familiar=f"{renda_total:.1f} Salários minimos",
            renda_per_capta=f"{renda_per_capta:.1f} Salários minimos",
        ).dict()

        return response
