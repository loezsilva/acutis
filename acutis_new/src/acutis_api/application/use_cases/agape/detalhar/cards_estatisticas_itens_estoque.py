from datetime import date  # Assuming date is sufficient for 'data' fields

from acutis_api.communication.responses.agape import (
    CardsEstatisticasItensEstoqueResponse,
)
from acutis_api.domain.repositories.agape import AgapeRepositoryInterface

# Placeholder imports for schemas - these will be defined in the next step
from acutis_api.domain.repositories.schemas.agape import (
    UltimaAcaoAgapeSchema,
    UltimaEntradaEstoqueSchema,
)


class CardsEstatisticasItensEstoqueUseCase:
    def __init__(self, repository: AgapeRepositoryInterface):
        self.__repository = repository

    def execute(
        self,
    ) -> CardsEstatisticasItensEstoqueResponse:
        quantidade_itens_em_estoque = (
            self.__repository.contagem_itens_estoque()
        )
        dados_ultima_acao: UltimaAcaoAgapeSchema = (
            self.__repository.ultima_acao_agape_com_itens()
        )
        dados_ultima_entrada: UltimaEntradaEstoqueSchema = (
            self.__repository.ultima_entrada_estoque()
        )

        ultima_acao_str = 'Não possui'
        if dados_ultima_acao:
            data_acao_val = getattr(dados_ultima_acao, 'data', None)
            qtd_acao_val = getattr(
                dados_ultima_acao, 'quantidade_itens_doados', None
            )
            if data_acao_val is not None and qtd_acao_val is not None:
                if isinstance(data_acao_val, (date,)):
                    ultima_acao_str = f"""
                        {data_acao_val.strftime('%d/%m/%Y')}
                        | {qtd_acao_val} Itens
                    """
                else:
                    ultima_acao_str = f'Data inválida | {qtd_acao_val} Itens'

        ultima_entrada_str = 'Não possui'
        if dados_ultima_entrada:
            data_entrada_val = getattr(dados_ultima_entrada, 'data', None)
            qtd_entrada_val = getattr(dados_ultima_entrada, 'quantidade', None)
            if data_entrada_val is not None and qtd_entrada_val is not None:
                if isinstance(data_entrada_val, (date,)):
                    ultima_entrada_str = f"""
                        {data_entrada_val.strftime('%d/%m/%Y')}
                        | {qtd_entrada_val} Itens
                    """
                else:
                    ultima_entrada_str = f"""
                        Data inválida
                        | {qtd_entrada_val} Itens
                    """

        # Create Response
        response_data = CardsEstatisticasItensEstoqueResponse(
            itens_em_estoque=f'{quantidade_itens_em_estoque} | Em estoque',
            ultima_acao=ultima_acao_str,
            ultima_entrada=ultima_entrada_str,
        ).model_dump()

        return response_data
