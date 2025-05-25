from datetime import datetime

from acutis_api.communication.responses.admin_graficos_cadastros import (
    MembrosPorHoraSchema,
)
from acutis_api.domain.repositories.admin_graficos_cadastros import (
    GraficosCadastrosRepositoryInterface,
)


class MembrosPorHoraDiaAtualUseCase:
    def __init__(self, repository: GraficosCadastrosRepositoryInterface):
        self.__repository = repository

    def execute(self) -> list[MembrosPorHoraSchema]:
        consulta = self.__repository.quantidade_membros_por_hora_dia_atual()

        dados_por_hora = {
            registro.hora: registro.quantidade_membro for registro in consulta
        }

        hora_atual = datetime.now().hour

        return [
            MembrosPorHoraSchema(
                hora=f'{hora:02d}:00', quantidade=dados_por_hora.get(hora, 0)
            )
            for hora in range(0, hora_atual + 1)
        ]
