from acutis_api.communication.responses.agape import (
    CardsEstatisticasFamiliasAgapeResponse,
)
from acutis_api.domain.repositories.agape import AgapeRepositoryInterface

# Placeholder imports for schemas - these will be defined in the next step
from acutis_api.domain.repositories.schemas.agape import (
    InformacoesAgregadasFamiliasSchema,
    NumeroTotalMembrosSchema,
    SomaTotalRendaSchema,
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
        dados_membros: NumeroTotalMembrosSchema = (
            self.__repository.numero_total_membros_agape()
        )
        dados_renda: SomaTotalRendaSchema = (
            self.__repository.soma_total_renda_familiar_agape()
        )

        total_cadastradas = getattr(dados_familias, 'total_cadastradas', 0)
        total_ativas = getattr(dados_familias, 'total_ativas', 0)
        total_inativas = getattr(dados_familias, 'total_inativas', 0)

        quantidade_total_membros = getattr(
            dados_membros, 'quantidade_total_membros', 0
        )

        soma_total_renda = getattr(dados_renda, 'soma_total_renda', 0.0)

        # Calculate Statistics
        media_membros = (
            (quantidade_total_membros / total_cadastradas)
            if total_cadastradas > 0
            else 0.0
        )

        renda_media_sm = 0.0
        if total_cadastradas > 0 and soma_total_renda > 0:
            renda_media_sm = (
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
            renda_media=f'{renda_media_sm:.1f} Salários minimos',
            membros_por_familia=f'{media_membros:.1f} pessoas',
            familias_ativas=f'{total_ativas} - {porcent_familias_ativas:.0f}%',
            familias_inativas=(
                f'{total_inativas} - {porcent_familias_inativas:.0f}%'
            ),
        ).model_dump()
