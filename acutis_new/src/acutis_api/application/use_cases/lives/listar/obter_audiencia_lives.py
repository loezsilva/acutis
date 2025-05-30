from typing import List

from acutis_api.communication.requests.lives import ObterAudienciaLivesRequest
from acutis_api.communication.responses.lives import (
    AudienciaLiveResponseItem,
    ObterAudienciaLivesResponse,
)
from acutis_api.domain.repositories.lives import LivesRepositoryInterface
from acutis_api.exception.errors.not_found import HttpNotFoundError


class ObterAudienciaLivesUseCase:
    def __init__(
        self, lives_repository: LivesRepositoryInterface
    ) -> list[ObterAudienciaLivesResponse]:
        self.lives_repository = lives_repository

    def execute(self, request: ObterAudienciaLivesRequest) -> List[dict]:
        audiencia = self.lives_repository.obter_audiencia_lives(request)

        if not audiencia:
            raise HttpNotFoundError(
                'Nenhuma audiência encontrada para esta live.'
            )

        response = [
            AudienciaLiveResponseItem(
                titulo=item.titulo,
                data_hora=item.data_hora_registro.strftime(
                    '%Y-%m-%d %H:%M:%S'
                ),
                audiencia=item.audiencia,
            ).model_dump()
            for item in audiencia
        ]

        return response
