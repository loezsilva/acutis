from acutis_api.communication.responses.agape import (
    BuscarCicloAcaoAgapeResponse,
    DoacaoAgapeResponse,
)
from acutis_api.domain.entities.endereco import Endereco
from acutis_api.domain.repositories.agape import AgapeRepositoryInterface


class BuscarCicloAcaoAgapeUseCase:
    """
    Busca detalhes de um ciclo de ação Ágape pelo ID da instância.
    """

    def __init__(self, agape_repository: AgapeRepositoryInterface):
        self._repository = agape_repository

    def execute(self, acao_agape_id):
        ciclo_acao_agape = self._repository.buscar_ciclo_acao_agape_por_id(
            acao_agape_id
        )

        endereco: Endereco = self._repository.buscar_endereco_ciclo_acao_agape(
            acao_agape_id
        )
        doacoes = self._repository.buscar_doacoes_ciclo_acao_agape(
            acao_agape_id
        )

        # Prepara lista de doações para resposta
        lista_doacoes = [
            DoacaoAgapeResponse(
                id=doacao.id,
                item_id=doacao.item_id,
                quantidade=doacao.quantidade,
                item=doacao.item,
            ).model_dump()
            for doacao in doacoes
        ]

        # Prepara resposta completa
        response = BuscarCicloAcaoAgapeResponse(
            id=ciclo_acao_agape.fk_acao_agape_id,
            abrangencia=ciclo_acao_agape.abrangencia,
            endereco=endereco,
            doacoes=lista_doacoes,
        ).model_dump()

        return response
