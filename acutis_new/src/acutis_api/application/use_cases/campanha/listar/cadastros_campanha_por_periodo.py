import uuid
from datetime import datetime, timedelta

from acutis_api.communication.responses.campanha import (
    CadastrosCampanhaPorPeriodoResponse,
)
from acutis_api.domain.repositories.campanha import CampanhaRepositoryInterface


class CadastrosCampanhaPorPeriodoUseCase:
    def __init__(self, repository: CampanhaRepositoryInterface):
        self.repository = repository

    def execute(
        self, campanha_id: uuid.UUID
    ) -> CadastrosCampanhaPorPeriodoResponse:
        agora = datetime.now()

        inicio_24h = agora - timedelta(hours=24)
        inicio_7_dias = agora - timedelta(days=7)
        inicio_30_dias = agora - timedelta(days=30)

        num_cadastros_24h = self.repository.buscar_cadastros_campanha_periodo(
            fk_campanha_id=campanha_id,
            inicio=inicio_24h,
            fim=agora,
        )

        num_cadastros_7d = self.repository.buscar_cadastros_campanha_periodo(
            fk_campanha_id=campanha_id,
            inicio=inicio_7_dias,
            fim=agora,
        )

        num_cadastros_30d = self.repository.buscar_cadastros_campanha_periodo(
            fk_campanha_id=campanha_id,
            inicio=inicio_30_dias,
            fim=agora,
        )

        return CadastrosCampanhaPorPeriodoResponse(
            ultimas_24h=num_cadastros_24h,
            ultimos_7_dias=num_cadastros_7d,
            ultimo_mes=num_cadastros_30d,
        ).model_dump()
