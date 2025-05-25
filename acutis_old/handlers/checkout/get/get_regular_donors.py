from datetime import date
from http import HTTPStatus
from flask import request
from dateutil.relativedelta import relativedelta
from models.schemas.checkout.get.get_regular_donors import (
    GetRegularDonorsQueryFilter,
    GetRegularDonorsResponse,
    RegularDonorSchema,
)
from repositories.checkout_repository import CheckoutRepository
from utils.functions import get_current_time


class GetRegularDonors:
    def __init__(self, repository: CheckoutRepository) -> None:
        self.__repository = repository

    def execute(self):
        filtros = GetRegularDonorsQueryFilter.parse_obj(request.args)

        data_atual = get_current_time().date()
        mes_inicial = (
            data_atual - relativedelta(months=filtros.quantidade_meses)
        ).replace(day=1)
        mes_final = data_atual.replace(day=1) - relativedelta(days=1)

        doadores_assiduos = self.__repository.get_regular_donors(
            filtros, mes_inicial, mes_final
        )
        dict_ranking_doadores_assiduos = self.__format_regular_donors(
            doadores_assiduos, mes_final, filtros
        )

        response = self.__prepare_response(dict_ranking_doadores_assiduos)
        return response, HTTPStatus.OK

    def __format_regular_donors(
        self,
        doadores_assiduidade,
        mes_final: date,
        filtros: GetRegularDonorsQueryFilter,
    ):
        inicio = (filtros.page - 1) * filtros.per_page
        fim = inicio + filtros.per_page

        ultimos_meses = []
        meses = filtros.quantidade_meses

        for i in range(1, meses):
            mes = mes_final.month - i
            ano = mes_final.year

            if mes <= 0:
                mes += 12
                ano -= 1
            ultimos_meses.append((ano, mes))

        doadores_assiduos = {}

        for doador in doadores_assiduidade:
            nome_doador = doador.nome
            fk_clifor_id = doador.fk_clifor_id
            mes = doador.mes
            ano = doador.ano
            doacoes_mes = doador.doacoes_mes

            if fk_clifor_id not in doadores_assiduos:
                doadores_assiduos[fk_clifor_id] = {
                    "benfeitor": nome_doador.title(),
                    "fk_usuario_id": doador.fk_usuario_id,
                    "meses": {
                        f"{ano}-{str(m).zfill(2)}": False
                        for (ano, m) in ultimos_meses
                    },
                    "total_doacoes": 0,
                }

            if doacoes_mes > 0:
                doadores_assiduos[fk_clifor_id]["total_doacoes"] += 1
                doadores_assiduos[fk_clifor_id]["meses"][
                    f"{ano}-{str(mes).zfill(2)}"
                ] = True

        doadores_ordenados = sorted(
            doadores_assiduos.values(),
            key=lambda x: x["total_doacoes"],
            reverse=True,
        )

        ranking_doadores_assiduos = doadores_ordenados[inicio:fim]

        for doador in ranking_doadores_assiduos:
            doador["doacoes"] = f"{doador['total_doacoes']}/{meses}"
            del doador["total_doacoes"]

        total_doadores = len(doadores_ordenados)
        total_paginas = (
            total_doadores + filtros.per_page - 1
        ) // filtros.per_page

        dict_ranking_doadores_assiduos = {
            "doadores": ranking_doadores_assiduos,
            "total": total_doadores,
            "total_paginas": total_paginas,
            "pagina_atual": filtros.page,
        }

        return dict_ranking_doadores_assiduos

    def __prepare_response(
        self,
        dict_ranking_doadores_assiduos,
    ):
        response = GetRegularDonorsResponse(
            total=dict_ranking_doadores_assiduos["total"],
            page=dict_ranking_doadores_assiduos["pagina_atual"],
            pages=dict_ranking_doadores_assiduos["total_paginas"],
            doadores_assiduos=[
                RegularDonorSchema(**doador).dict()
                for doador in dict_ranking_doadores_assiduos["doadores"]
            ],
        ).dict()

        return response
