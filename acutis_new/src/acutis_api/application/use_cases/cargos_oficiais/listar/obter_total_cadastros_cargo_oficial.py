from acutis_api.communication.responses.cargos_oficiais import (
    ObterTotalCadastrosCargoOficialResponse,
    ObterTotalCadastrosCargoOficialSchema,
)
from acutis_api.domain.repositories.cargos_oficiais import (
    CargosOficiaisRepositoryInterface,
)


class ObterTotalCadastrosCargoOficialUseCase:
    def __init__(self, repository: CargosOficiaisRepositoryInterface):
        self.__repository = repository

    def execute(self) -> ObterTotalCadastrosCargoOficialResponse:
        resultados = self.__repository.obter_total_cadastros_cargo_oficial()

        resposta = [
            ObterTotalCadastrosCargoOficialSchema(
                nome_cargo=nome_cargo,
                total_cadastros_cargo=total_cadastros,
            )
            for nome_cargo, total_cadastros in resultados
        ]

        return ObterTotalCadastrosCargoOficialResponse(
            root=resposta
        ).model_dump()
