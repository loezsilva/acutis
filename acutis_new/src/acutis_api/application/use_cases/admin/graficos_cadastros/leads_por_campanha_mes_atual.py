from acutis_api.communication.responses.admin_graficos_cadastros import (
    LeadsPorOrigemSchema,
)
from acutis_api.domain.repositories.admin_graficos_cadastros import (
    GraficosCadastrosRepositoryInterface,
)


class LeadsPorCampanhaMesAtualUseCase:
    def __init__(self, repository: GraficosCadastrosRepositoryInterface):
        self.__repository = repository

    def execute(self) -> list[LeadsPorOrigemSchema]:
        leads_por_origem = self.__repository.leads_por_origem_mes_atual()
        return [
            LeadsPorOrigemSchema(**lead._asdict()) for lead in leads_por_origem
        ]
