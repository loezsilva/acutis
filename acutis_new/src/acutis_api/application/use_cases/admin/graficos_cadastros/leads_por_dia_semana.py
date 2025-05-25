from acutis_api.communication.responses.admin_graficos_cadastros import (
    LeadsPorDiaSemanaSchema,
)
from acutis_api.domain.repositories.admin_graficos_cadastros import (
    GraficosCadastrosRepositoryInterface,
)


class LeadsPorDiaSemanaUseCase:
    def __init__(self, repository: GraficosCadastrosRepositoryInterface):
        self.__repository = repository

    def execute(self):
        consulta = self.__repository.leads_por_dia_semana()

        dias_semana = {
            1: 'domingo',
            2: 'segunda',
            3: 'terça',
            4: 'quarta',
            5: 'quinta',
            6: 'sexta',
            7: 'sabado',
        }

        resposta = []
        for item in consulta:
            resposta.append(
                LeadsPorDiaSemanaSchema(
                    dia_semana=dias_semana[item[0]],
                    quantidade=item[1],
                ).model_dump()
            )

        return resposta
