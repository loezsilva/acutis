from acutis_api.communication.responses.lives import (
    ObterDatasLivesOcorridasResponse,
)
from acutis_api.domain.repositories.lives import LivesRepositoryInterface
from acutis_api.exception.errors.not_found import HttpNotFoundError


class ObterDatasLivesOcorridasUseCase:
    def __init__(self, repository: LivesRepositoryInterface):
        self.repository = repository

    def execute(self) -> ObterDatasLivesOcorridasResponse:
        datas = self.repository.obter_datas_lives_ocorridas()

        if not datas:
            raise HttpNotFoundError('Nenhuma data encontrada')

        return ObterDatasLivesOcorridasResponse(
            datas=[data.strftime('%Y-%m-%d') for data in datas]
        )
