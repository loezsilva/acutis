from acutis_api.communication.responses.admin_graficos_cadastros import (
    LeadsPorHoraSchema,
)
from acutis_api.domain.repositories.admin_graficos_cadastros import (
    GraficosCadastrosRepositoryInterface,
)


class QuantidadeLeadsPorHoraUseCase:
    def __init__(self, repository: GraficosCadastrosRepositoryInterface):
        self.__repository = repository

    def execute(self) -> list[LeadsPorHoraSchema]:
        consulta = self.__repository.quantidade_leads_por_hora()

        leads_por_hora = []

        for registro in consulta:
            leads_por_hora.append(
                LeadsPorHoraSchema(
                    hora=f'{registro[0]:02d}', quantidade=registro[1]
                )
            )

        return leads_por_hora
