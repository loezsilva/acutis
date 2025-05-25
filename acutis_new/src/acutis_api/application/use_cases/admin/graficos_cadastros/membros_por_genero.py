from acutis_api.communication.responses.admin_graficos_cadastros import (
    MembrosPorGeneroResponse,
)
from acutis_api.domain.repositories.admin_graficos_cadastros import (
    GraficosCadastrosRepositoryInterface,
)


class QuantidadeMembrosPorGeneroUseCase:
    def __init__(self, repository: GraficosCadastrosRepositoryInterface):
        self.__repository = repository

    def execute(self) -> dict[MembrosPorGeneroResponse]:
        consulta = self.__repository.quantidade_membros_por_genero()
        resultado = {'masculino': 0, 'feminino': 0, 'outros': 0}

        total = 0
        for genero, quantidade in consulta:
            key = genero.value if genero is not None else 'outros'
            resultado[key] += quantidade
            total += quantidade

        resultado_com_porcentagem = {}
        for genero, quantidade in resultado.items():
            porcentagem = (quantidade / total) * 100 if total > 0 else 0
            resultado_com_porcentagem[genero] = {
                'quantidade': quantidade,
                'porcentagem': round(porcentagem, 2),
            }

        return resultado_com_porcentagem
