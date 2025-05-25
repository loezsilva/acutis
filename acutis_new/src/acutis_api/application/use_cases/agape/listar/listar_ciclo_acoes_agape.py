import math

from acutis_api.communication.requests.agape import (
    ListarCiclosAcoesAgapeQueryPaginada,
)
from acutis_api.communication.responses.agape import (
    InstanciaCicloAgapeResponse,
    ListarCiclosAcoesAgapeResponsePaginada,
)
from acutis_api.domain.repositories.agape import AgapeRepositoryInterface


class ListarCicloAcoesAgapeUseCase:
    """
    Caso de uso para listar ações Ágape com contagem de ciclos finalizados:
    - Filtra por ID de ação e intervalo de datas
    - Retorna lista paginada com total de ciclos finalizados
    """

    def __init__(
        self,
        agape_repository: AgapeRepositoryInterface,
    ):
        self.__repository = agape_repository

    def execute(
        self, filtros: ListarCiclosAcoesAgapeQueryPaginada
    ) -> ListarCiclosAcoesAgapeResponsePaginada:
        # Executa consulta ao repositório para obter instâncias do ciclo
        instancias, total = self.__repository.listar_ciclos_acao(filtros)

        # Cria resposta paginada
        pagina_atual = filtros.pagina
        paginas_total = (
            math.ceil(total / filtros.por_pagina) if filtros.por_pagina else 1
        )

        return ListarCiclosAcoesAgapeResponsePaginada(
            pagina=pagina_atual,
            paginas=paginas_total,
            total=total,
            resultados=[
                InstanciaCicloAgapeResponse(
                    id=instancia.id,
                    abrangencia=instancia.abrangencia,
                    acao_id=instancia.fk_acao_agape_id,
                    endereco_id=instancia.fk_endereco_id,
                    data_inicio=instancia.data_inicio,
                    data_termino=instancia.data_termino,
                    status=instancia.status,
                ).model_dump()
                for instancia in instancias
            ],
        )
