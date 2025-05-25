import math

from acutis_api.communication.requests.agape import (
    ListarItensEstoqueAgapeQueryPaginada,
)
from acutis_api.communication.responses.agape import (
    ItemEstoqueAgapeResponse,
    ListarItensEstoqueAgapeResponsePaginada,
)
from acutis_api.domain.repositories.agape import (
    AgapeRepositoryInterface,
)


class ListarItensEstoqueAgapeUseCase:
    def __init__(
        self,
        repository: AgapeRepositoryInterface,
    ):
        self.__repository = repository

    def execute(self, filtros: ListarItensEstoqueAgapeQueryPaginada):
        itens, total = self.__repository.listar_itens_estoque_agape(filtros)

        response = ListarItensEstoqueAgapeResponsePaginada(
            pagina=filtros.pagina,
            paginas=math.ceil(total / filtros.por_pagina),
            total=total,
            resultados=[
                ItemEstoqueAgapeResponse(
                    id=item.id,
                    item=item.item,
                    quantidade=item.quantidade,
                )
                for item in itens
            ],
        )

        return response
