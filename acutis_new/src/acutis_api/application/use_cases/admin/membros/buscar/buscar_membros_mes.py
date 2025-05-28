from datetime import datetime, timedelta

from acutis_api.communication.responses.admin_membros import (
    BuscarMembrosMesResponse,
)
from acutis_api.domain.repositories.admin_membros import (
    AdminMembrosRepositoryInterface,
)


class BuscarMembrosMesUseCase:
    def __init__(self, repository: AdminMembrosRepositoryInterface):
        self._repository = repository

    def execute(self) -> dict:
        hoje = datetime.now()

        membros_mes_atual = self._repository.buscar_membros_mes(hoje)

        data_mes_anterior = hoje.replace(day=1) - timedelta(days=1)

        membros_mes_anterior = self._repository.buscar_membros_mes(
            data_mes_anterior
        )

        if membros_mes_anterior > 0:
            crescimento = (
                (membros_mes_atual - membros_mes_anterior)
                / membros_mes_anterior
            ) * 100
        else:
            crescimento = 0.0

        porcentagem_crescimento = round(crescimento, 2)

        response = BuscarMembrosMesResponse(
            membros_mes=membros_mes_atual,
            porcentagem_crescimento=porcentagem_crescimento,
        ).model_dump()

        return response
