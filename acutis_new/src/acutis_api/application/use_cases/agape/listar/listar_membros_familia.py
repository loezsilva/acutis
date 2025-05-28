import math

from acutis_api.application.utils.funcoes_auxiliares import calcular_idade
from acutis_api.communication.responses.agape import (
    ListarMembrosFamiliaAgapeResponsePaginada,
    MembroFamiliaAgapeResponse,
)
from acutis_api.domain.repositories.agape import AgapeRepositoryInterface
from acutis_api.domain.repositories.schemas.agape import (
    ListarMembrosFamiliaAgapeFiltros,
)


class ListarMembrosFamiliaUseCase:
    """
    Caso de uso para listar as famílias cadastradas:
    """

    def __init__(
        self,
        agape_repository: AgapeRepositoryInterface,
    ):
        self.__repository = agape_repository

    def execute(
        self, filtros: ListarMembrosFamiliaAgapeFiltros
    ) -> ListarMembrosFamiliaAgapeResponsePaginada:
        # Executa consulta ao repositório para obter instâncias do ciclo
        instancias, total = self.__repository.listar_membros_familia(
            familia_id=filtros.familia_id
        )

        # Cria resposta paginada
        pagina_atual = filtros.pagina
        paginas_total = (
            math.ceil(total / filtros.por_pagina) if filtros.por_pagina else 1
        )

        return ListarMembrosFamiliaAgapeResponsePaginada(
            pagina=pagina_atual,
            paginas=paginas_total,
            total=total,
            resultados=[
                MembroFamiliaAgapeResponse(
                    id=instancia.id,
                    cpf=instancia.cpf,
                    nome=instancia.nome,
                    email=instancia.email,
                    telefone=instancia.telefone,
                    ocupacao=instancia.ocupacao,
                    renda=instancia.renda,
                    responsavel=instancia.responsavel,
                    idade=calcular_idade(instancia.data_nascimento),
                ).model_dump()
                for instancia in instancias
            ],
        )
