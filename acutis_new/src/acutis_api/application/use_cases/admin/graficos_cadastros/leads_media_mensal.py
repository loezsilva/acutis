from acutis_api.domain.repositories.admin_graficos_cadastros import (
    GraficosCadastrosRepositoryInterface,
)


class LeadsMediaMensalUseCase:
    def __init__(
        self, repository: GraficosCadastrosRepositoryInterface
    ) -> int:
        self.__repository = repository

    def execute(self) -> float:
        return self.__repository.media_mensal_leads()
