from acutis_api.communication.requests.lives import (
    ObterLivesProgramadasRequest,
)
from acutis_api.communication.responses.lives import (
    ListaObterLivesProgramadasResponse,
    ObterLivesProgramadasResponse,
)
from acutis_api.domain.repositories.lives import LivesRepositoryInterface
from acutis_api.exception.errors.not_found import HttpNotFoundError


class ObterLivesProgramadasUseCase:
    def __init__(
        self, lives_repository: LivesRepositoryInterface
    ) -> list[ObterLivesProgramadasResponse]:
        self.lives_repository = lives_repository

    def execute(self, request: ObterLivesProgramadasRequest):
        lives = self.lives_repository.obter_lives_programadas(request)

        if not lives:
            raise HttpNotFoundError('Não foram encontradas lives programadas.')

        response = ListaObterLivesProgramadasResponse(
            ObterLivesProgramadasResponse(
                id=live['id'],
                tag=live['tag'],
                rede_social=live['rede_social'],
                tipo_programacao=live['tipo_programacao'],
            )
            for live in lives
        )

        return response.model_dump()
