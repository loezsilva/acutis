from acutis_api.communication.responses.agape import (
    CardsEstatisticasFamiliasAgapeResponse,
)
from acutis_api.domain.repositories.agape import AgapeRepositoryInterface

# Placeholder imports for schemas - these will be defined in the next step
from acutis_api.domain.repositories.schemas.agape import (
    InformacoesAgregadasFamiliasSchema,
)

SALARIO_MINIMO = 1518.0


class CardsEstatisticasFamiliasAgapeUseCase:
    def __init__(self, repository: AgapeRepositoryInterface):
        self.__repository = repository

    def execute(
        self,
    ) -> CardsEstatisticasFamiliasAgapeResponse:
        dados_familias: InformacoesAgregadasFamiliasSchema = (
            self.__repository.informacoes_agregadas_familias()
        )
        quantidade_total_membros = (
            self.__repository.numero_total_membros_agape()
        )
        soma_total_renda = self.__repository.soma_total_renda_familiar_agape()

        total_cadastradas = dados_familias.total_cadastradas
        total_ativas = dados_familias.total_ativas
        total_inativas = dados_familias.total_inativas

        # Calculate Statistics
        media_membros = (
            (quantidade_total_membros / total_cadastradas)
            if total_cadastradas > 0
            else 0.0
        )

        soma_renda_media = 0.0
        if total_cadastradas > 0 and soma_total_renda > 0:
            soma_renda_media = (
                soma_total_renda / total_cadastradas
            ) / SALARIO_MINIMO

        porcent_familias_ativas = (
            (total_ativas / total_cadastradas) * 100
            if total_cadastradas > 0
            else 0.0
        )
        porcent_familias_inativas = (
            (total_inativas / total_cadastradas) * 100
            if total_cadastradas > 0
            else 0.0
        )

        return CardsEstatisticasFamiliasAgapeResponse(
            familias_cadastradas=f'{total_ativas} - Famílias ativas',
            renda_media=f'{soma_renda_media:.1f} Salários minimos',
            membros_por_familia=f'{media_membros:.1f} pessoas',
            familias_ativas=f'{total_ativas} - {porcent_familias_ativas:.0f}%',
            familias_inativas=(
                f'{total_inativas} - {porcent_familias_inativas:.0f}%'
            ),
        ).model_dump()
