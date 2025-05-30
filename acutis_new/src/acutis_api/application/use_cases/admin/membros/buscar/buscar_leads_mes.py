from datetime import datetime

from acutis_api.application.utils.funcoes_auxiliares import buscar_data_valida
from acutis_api.communication.responses.admin_membros import (
    BuscarLeadsMesResponse,
)
from acutis_api.domain.repositories.admin_membros import (
    AdminMembrosRepositoryInterface,
)


class BuscarLeadsMesUseCase:
    def __init__(self, repository: AdminMembrosRepositoryInterface):
        self._repository = repository

    def execute(self) -> dict:
        hoje = datetime.now()

        primeiro_dia_mes = hoje.replace(day=1)
        leads_mes_atual = self._repository.buscar_leads_periodo(
            primeiro_dia_mes, hoje
        )

        ano = hoje.year
        mes = hoje.month - 1
        if mes == 0:
            mes = 12
            ano -= 1

        dia = hoje.day
        data_mes_anterior = buscar_data_valida(dia, mes, ano)

        data_mes_anterior = datetime.combine(
            data_mes_anterior, datetime.max.time()
        )

        inicio_mes_anterior = data_mes_anterior.replace(day=1)

        leads_mes_anterior = self._repository.buscar_leads_periodo(
            inicio_mes_anterior, data_mes_anterior
        )

        if leads_mes_anterior > 0:
            crescimento = (
                (leads_mes_atual - leads_mes_anterior) / leads_mes_anterior
            ) * 100
        else:
            crescimento = 0.0

        porcentagem_crescimento = round(crescimento, 2)

        response = BuscarLeadsMesResponse(
            leads_mes=leads_mes_atual,
            porcentagem_crescimento=porcentagem_crescimento,
        ).model_dump()

        return response
