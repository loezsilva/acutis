from acutis_api.domain.repositories.admin_graficos_cadastros import (
    GraficosCadastrosRepositoryInterface,
)


class MembrosPorPaisUseCase:
    def __init__(self, repository: GraficosCadastrosRepositoryInterface):
        self.__repository = repository

    def execute(self) -> dict[str, int]:
        consulta = self.__repository.membros_por_pais()

        response = {}

        for pais in consulta:
            pais_key = pais.pais if pais.pais is not None else 'NaN'
            response[pais_key] = pais.quantidade

        return response
