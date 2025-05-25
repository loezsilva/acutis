from acutis_api.communication.responses.admin_graficos_cadastros import (
    LeadsPorEvolucaoMensalSchema,
)
from acutis_api.domain.repositories.admin_graficos_cadastros import (
    GraficosCadastrosRepositoryInterface,
)


class LeadsPorEvolucaoMensalUseCase:
    def __init__(self, repository: GraficosCadastrosRepositoryInterface):
        self.__repository = repository

    def execute(self) -> list[LeadsPorEvolucaoMensalSchema]:
        consulta = self.__repository.leads_por_evolucao_mensal()
        return [
            LeadsPorEvolucaoMensalSchema(**item._asdict()) for item in consulta
        ]
