from acutis_api.communication.responses.admin_graficos_cadastros import (
    MembrosPorIdadeSchema,
)
from acutis_api.domain.repositories.admin_graficos_cadastros import (
    GraficosCadastrosRepositoryInterface,
)


class CadastrosPorIdadeUseCase:
    def __init__(self, repository: GraficosCadastrosRepositoryInterface):
        self.__repository = repository

    def execute(self) -> list[MembrosPorIdadeSchema]:
        dados_brutos = self.__repository.quantidade_membros_por_idade()

        return [
            MembrosPorIdadeSchema(
                faixa_etaria=item.faixa_etaria,
                masculino=item.masculino,
                feminino=item.feminino,
                nao_informado=item.nao_informado,
            )
            for item in dados_brutos
        ]
