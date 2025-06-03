import math
import uuid

from acutis_api.application.utils.funcoes_auxiliares import calcular_idade
from acutis_api.communication.responses.agape import (
    ListarMembrosFamiliaAgapeResponsePaginada,
    MembroFamiliaAgapeResponse,
)
from acutis_api.domain.repositories.agape import AgapeRepositoryInterface
from acutis_api.domain.repositories.schemas.agape import (
    ListarMembrosFamiliaAgapeFiltros,
)
from acutis_api.exception.errors.not_found import HttpNotFoundError


class ListarMembrosFamiliaUseCase:
    """
    Caso de uso para listar membros de uma familia:
    """

    def __init__(
        self,
        agape_repository: AgapeRepositoryInterface,
    ):
        self.__repository = agape_repository

    def execute(
        self, filtros: ListarMembrosFamiliaAgapeFiltros, familia_id: uuid.UUID
    ) -> ListarMembrosFamiliaAgapeResponsePaginada:
        familia = self.__repository.buscar_familia_por_id(familia_id)

        if familia is None:
            raise HttpNotFoundError('Família não encontrada.')

        instancias, total = self.__repository.listar_membros_familia(
            filtros=filtros, familia_id=familia_id
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
