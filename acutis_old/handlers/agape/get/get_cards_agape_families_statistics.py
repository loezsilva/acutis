from http import HTTPStatus
from typing import Dict
from models.schemas.agape.get.get_cards_agape_families_statistics import (
    GetCardsAgapeFamiliesStatisticsResponse,
)
from repositories.interfaces.agape_repository_interface import (
    AgapeRepositoryInterface,
)
from repositories.schemas.agape_schemas import (
    GetAgapeFamiliesInfoSchema,
    GetNumberRegisteredAgapeMembersSchema,
    GetSumAgapeFamiliesIncomeSchema,
)


class GetCardsAgapeFamiliesStatistics:
    def __init__(self, respository: AgapeRepositoryInterface):
        self.__repository = respository

    def execute(self):
        familias = self.__repository.get_agape_families_info()
        membros_cadastrados = (
            self.__repository.get_number_registered_agape_families_members()
        )
        renda = self.__repository.get_sum_agape_families_income()
        response = self.__prepare_response(
            familias, membros_cadastrados, renda
        )

        return response, HTTPStatus.OK

    def __prepare_response(
        self,
        familias: GetAgapeFamiliesInfoSchema,
        membros_cadastrados: GetNumberRegisteredAgapeMembersSchema,
        renda: GetSumAgapeFamiliesIncomeSchema,
    ) -> Dict:
        salario_minimo = 1518
        media_membros = (
            membros_cadastrados.quantidade / familias.cadastradas
            if familias.cadastradas > 0
            else 0
        )
        renda_media = (renda.total / familias.cadastradas) / salario_minimo if renda.total > 0 else 0
        porcent_familias_ativas = (
            (familias.ativas / familias.cadastradas) * 100
            if familias.cadastradas > 0
            else 0
        )
        porcent_familias_inativas = (
            (familias.inativas / familias.cadastradas) * 100
            if familias.cadastradas > 0
            else 0
        )

        response = GetCardsAgapeFamiliesStatisticsResponse(
            familias_cadastradas=f"{familias.ativas} - Famílias ativas",
            renda_media=f"{renda_media:.1f} Salários minimos",
            membros_por_familia=f"{media_membros:.1f} pessoas",
            familias_ativas=f"{familias.ativas} - {porcent_familias_ativas:.0f}%",
            familias_inativas=f"{familias.inativas} - {porcent_familias_inativas:.0f}%",
        ).dict()

        return response
