from http import HTTPStatus
import math
from dateutil.relativedelta import relativedelta

from flask import request
from models.schemas.checkout.get.get_donors_ranking import (
    DonorRankingSchema,
    GetDonorsRankingQueryFilter,
    GetDonorsRankingResponse,
)
from repositories.checkout_repository import CheckoutRepository
from utils.functions import get_current_time


class GetDonorsRanking:
    def __init__(self, repository: CheckoutRepository) -> None:
        self.__repository = repository

    def execute(self):
        filtros = GetDonorsRankingQueryFilter.parse_obj(request.args)

        data_atual = get_current_time().date()
        mes_inicial = (
            data_atual - relativedelta(months=filtros.quantidade_meses)
        ).replace(day=1)
        mes_final = data_atual.replace(day=1) - relativedelta(days=1)

        ranking_doadores, total = self.__repository.get_donors_ranking(
            filtros, mes_inicial, mes_final
        )

        response = self.__prepare_response(ranking_doadores, total, filtros)
        return response, HTTPStatus.OK

    def __prepare_response(
        self,
        ranking_doadores: list[DonorRankingSchema],
        total: int,
        filtros: GetDonorsRankingQueryFilter,
    ) -> dict:
        response = GetDonorsRankingResponse(
            total=total,
            page=filtros.page,
            pages=math.ceil(total / filtros.per_page),
            doadores=[
                DonorRankingSchema.from_orm(doador).dict()
                for doador in ranking_doadores
            ],
        ).dict()

        return response
