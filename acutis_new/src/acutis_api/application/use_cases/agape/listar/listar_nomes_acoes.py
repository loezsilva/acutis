import math

from acutis_api.communication.requests.agape import (
    ListarNomesAcoesAgapeQueryPaginada,
)
from acutis_api.communication.responses.agape import (
    AcaoAgapeResponse,
    ListarNomesAcoesAgapeResponsePaginada,
)
from acutis_api.domain.repositories.agape import (
    AgapeRepositoryInterface,
)


class ListarNomesAcoesAgapeUseCase:
    def __init__(
        self,
        repository: AgapeRepositoryInterface,
    ):
        self.__repository = repository

    def execute(self, filtros: ListarNomesAcoesAgapeQueryPaginada):
        nomes_acoes_agape, total = self.__repository.listar_nomes_acoes_agape(
            filtros
        )

        response = ListarNomesAcoesAgapeResponsePaginada(
            pagina=filtros.pagina,
            paginas=math.ceil(total / filtros.por_pagina),
            total=total,
            resultados=[
                AcaoAgapeResponse(
                    id=nome_acao_agape.id,
                    nome=nome_acao_agape.nome,
                )
                for nome_acao_agape in nomes_acoes_agape
            ],
        )

        return response
