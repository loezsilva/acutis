from acutis_api.communication.responses.admin_graficos_cadastros import (
    QuantidadeLeadsPorOrigemSchema,
)
from acutis_api.domain.repositories.admin_graficos_cadastros import (
    GraficosCadastrosRepositoryInterface,
)


class LeadsPorOrigemUseCase:
    def __init__(self, repository: GraficosCadastrosRepositoryInterface):
        self.__repository = repository

    def execute(self):
        consulta = self.__repository.leads_por_origem()
        total = self.__repository.quantidade_leads_total()

        resposta = []
        for item in consulta:
            porcentagem = (item.quantidade / total) * 100 if total > 0 else 0
            resposta.append(
                QuantidadeLeadsPorOrigemSchema(
                    origem=item.origem_cadastro,
                    quantidade=item.quantidade,
                    porcentagem=round(porcentagem, 2),
                ).model_dump()
            )

        return resposta
