from acutis_api.communication.requests.lives import ObterCanalRequest
from acutis_api.communication.responses.lives import (
    ListaObterCanalResponse,
    ObterCanalSchema,
)
from acutis_api.domain.repositories.lives import LivesRepositoryInterface
from acutis_api.exception.errors.not_found import HttpNotFoundError


class ObterCanalUseCase:
    def __init__(self, lives_repository: LivesRepositoryInterface):
        self.lives_repository = lives_repository

    def execute(self, request: ObterCanalRequest):
        canais = self.lives_repository.obter_canal(request)

        if not canais:
            raise HttpNotFoundError(
                'Não foram encontrados canais cadastrados.'
            )

        response = ListaObterCanalResponse([
            ObterCanalSchema(
                id=canal.id, tag=canal.tag, rede_social=canal.rede_social
            )
            for canal in canais
        ])

        return response.model_dump()
