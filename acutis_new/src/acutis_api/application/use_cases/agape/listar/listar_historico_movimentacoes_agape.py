import math  # Para cálculo do total de páginas

from acutis_api.communication.requests.agape import (
    ListarHistoricoMovimentacoesAgapeQueryPaginada,
)
from acutis_api.communication.responses.agape import (
    HistoricoMovimentacaoItemAgapeResponse,
    ListarHistoricoMovimentacoesAgapeResponsePaginada,
)
from acutis_api.domain.repositories.agape import AgapeRepositoryInterface


class ListarHistoricoMovimentacoesAgapeUseCase:
    def __init__(self, agape_repository: AgapeRepositoryInterface):
        self.agape_repository = agape_repository

    def execute(
        self, filtros: ListarHistoricoMovimentacoesAgapeQueryPaginada
    ) -> ListarHistoricoMovimentacoesAgapeResponsePaginada:
        """
        Executa a lógica para listar o histórico de movimentações.
        """

        movimentacoes_query = (
            self.agape_repository.listar_historico_movimentacoes_paginado(
                filtros
            )
        )

        movimentacoes, total = self.agape_repository.query_paginada(
            movimentacoes_query, filtros.pagina, filtros.por_pagina
        )

        resultados_resposta = []
        for movimentacao in movimentacoes:
            resultados_resposta.append(
                HistoricoMovimentacaoItemAgapeResponse(
                    id=movimentacao.id,
                    item_id=movimentacao.item_id,
                    nome_item=movimentacao.item,
                    quantidade=movimentacao.quantidade,
                    tipo_movimentacao=movimentacao.tipo_movimentacoes,
                    data_movimentacao=movimentacao.criado_em,
                )
            )

        return ListarHistoricoMovimentacoesAgapeResponsePaginada(
            pagina=filtros.pagina,
            paginas=math.ceil(total / filtros.por_pagina),
            total=total,
            resultados=resultados_resposta,
        ).model_dump()
