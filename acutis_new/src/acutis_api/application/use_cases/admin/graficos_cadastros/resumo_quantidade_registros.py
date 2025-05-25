from acutis_api.communication.requests.admin_graficos_cadastros import (
    ResumoQuantidadeRegistrosRequest,
)
from acutis_api.communication.responses.admin_graficos_cadastros import (
    ResumoQuantidadeRegistrosResponse,
)
from acutis_api.domain.repositories.admin_graficos_cadastros import (
    GraficosCadastrosRepositoryInterface,
)


class ResumoQuantidadeRegistrosUseCase:
    def __init__(self, repository: GraficosCadastrosRepositoryInterface):
        self.__repository = repository

    def execute(
        self, requisicao: ResumoQuantidadeRegistrosRequest
    ) -> ResumoQuantidadeRegistrosResponse:
        leads, membros, benfeitores = (
            self.__repository.resumo_quantidade_registros(requisicao)
        )

        return ResumoQuantidadeRegistrosResponse(
            leads=leads, membros=membros, benfeitores=benfeitores
        )
