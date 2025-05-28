import math  # Para cálculo do total de páginas
from http import HTTPStatus

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
    ) -> tuple[ListarHistoricoMovimentacoesAgapeResponsePaginada, HTTPStatus]:
        """
        Executa a lógica para listar o histórico de movimentações.
        """

        movimentacoes_com_nome_item, total_itens = (
            self.agape_repository.listar_historico_movimentacoes_paginado(
                pagina=filtros.pagina,
                por_pagina=filtros.por_pagina,
            )
        )

        resultados_response = []
        for mov_entity, nome_item_str in movimentacoes_com_nome_item:
            resultados_response.append(
                HistoricoMovimentacaoItemAgapeResponse(
                    id=mov_entity.id,
                    item_id=mov_entity.fk_estoque_agape_id,
                    nome_item=nome_item_str,  # Nome do item vindo do JOIN
                    quantidade=mov_entity.quantidade,
                    tipo_movimentacao=mov_entity.tipo_movimentacoes,
                    origem=mov_entity.origem,
                    destino=mov_entity.destino,
                    ciclo_acao_id=mov_entity.fk_instancia_acao_agape_id,
                    data_movimentacao=mov_entity.criado_em,
                )
            )

        total_paginas = (
            math.ceil(total_itens / filtros.por_pagina)
            if filtros.por_pagina > 0
            else 0
        )
        if total_paginas == 0 and total_itens > 0:
            total_paginas = 1

        response_paginada = ListarHistoricoMovimentacoesAgapeResponsePaginada(
            pagina=filtros.pagina,
            paginas=total_paginas,
            total=total_itens,
            resultados=resultados_response,
        )

        return response_paginada, HTTPStatus.OK
