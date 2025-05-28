from acutis_api.domain.repositories.admin_graficos_cadastros import (
    GraficosCadastrosRepositoryInterface,
)


class MembrosPorEstadoUseCase:
    def __init__(self, repository: GraficosCadastrosRepositoryInterface):
        self.__repository = repository

    def execute(self) -> dict[str, int]:
        consulta = self.__repository.membros_por_estado()

        response = {}

        for estado in consulta:
            estado_key = estado.estado if estado.estado is not None else 'NaN'
            response[estado_key] = estado.quantidade

        return response
