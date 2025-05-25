from datetime import datetime

from acutis_api.communication.responses.admin_graficos_cadastros import (
    MembrosPorMesSchema,
)
from acutis_api.domain.repositories.admin_graficos_cadastros import (
    GraficosCadastrosRepositoryInterface,
)


class MembrosPorDiaMesAtualUseCase:
    def __init__(self, repository: GraficosCadastrosRepositoryInterface):
        self.__repository = repository

    def execute(self) -> list[MembrosPorMesSchema]:
        consulta = self.__repository.quantidade_membros_por_dia_mes_atual()
        hoje = datetime.now()

        dados_por_dia = {
            registro.dia: registro.quantidade_membros for registro in consulta
        }

        return [
            MembrosPorMesSchema(
                dia=f'{dia:02d}-{hoje.month:02d}-{hoje.year}',
                quantidade=dados_por_dia.get(
                    f'{dia:02d}-{hoje.month:02d}-{hoje.year}', 0
                ),
            )
            for dia in range(1, hoje.day + 1)
        ]
