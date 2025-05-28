from datetime import datetime, timedelta

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

        leads_mes_atual = self._repository.buscar_leads_mes(hoje)

        data_mes_anterior = hoje.replace(day=1) - timedelta(days=1)

        leads_mes_anterior = self._repository.buscar_leads_mes(
            data_mes_anterior
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
