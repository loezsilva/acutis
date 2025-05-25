from http import HTTPStatus
from flask import request
from models.schemas.checkout.get.get_top_regular_donors import (
    GetTopRegularDonorsQueryFilter,
    GetTopRegularDonorsResponse,
    TopRegularDonorSchema,
)
from dateutil.relativedelta import relativedelta
from repositories.checkout_repository import CheckoutRepository
from services.file_service import FileService
from utils.functions import get_current_time


class GetTopRegularDonors:
    def __init__(
        self, repository: CheckoutRepository, file_service: FileService
    ) -> None:
        self.__repository = repository
        self.__file_service = file_service

    def execute(self):
        filtros = GetTopRegularDonorsQueryFilter.parse_obj(request.args)

        data_atual = get_current_time().date()
        mes_inicial = (
            data_atual - relativedelta(months=filtros.quantidade_meses)
        ).replace(day=1)
        mes_final = data_atual.replace(day=1) - relativedelta(days=1)

        top_doadores = self.__repository.get_top_regular_donors(
            filtros, mes_inicial, mes_final
        )
        top_doadores_formatados = self.__format_top_donors(top_doadores)
        response = self.__prepare_response(top_doadores_formatados)

        return response, HTTPStatus.OK

    def __format_top_donors(self, top_doadores: list[TopRegularDonorSchema]):
        doadores = []

        for index, doador in enumerate(top_doadores, start=1):
            info_doador = {
                "nome": f"{index}° {doador.nome.title()}",
                "avatar": (
                    self.__file_service.get_public_url(doador.avatar)
                    if doador.avatar
                    else None
                ),
                "fk_usuario_id": doador.fk_usuario_id,
            }
            doadores.append(info_doador)

        return doadores

    def __prepare_response(self, doadores: list[dict]):
        response = GetTopRegularDonorsResponse(
            top_doadores=[
                TopRegularDonorSchema(**doador).dict() for doador in doadores
            ]
        ).dict()

        return response
