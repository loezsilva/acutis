from acutis_api.communication.responses.admin_graficos_cadastros import (
    CadastroPormesSchema,
)
from acutis_api.domain.repositories.admin_graficos_cadastros import (
    GraficosCadastrosRepositoryInterface,
)


class CadastrosPorMesUseCase:
    def __init__(self, repository: GraficosCadastrosRepositoryInterface):
        self.__repository = repository

    def execute(self):
        consulta = self.__repository.quantidade_leads_por_mes()

        return [
            CadastroPormesSchema(**cadastro._asdict()) for cadastro in consulta
        ]
