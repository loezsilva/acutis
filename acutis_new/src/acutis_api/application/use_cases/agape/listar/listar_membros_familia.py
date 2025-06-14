import math
import uuid

from flask import request

from acutis_api.application.utils.funcoes_auxiliares import calcular_idade
from acutis_api.communication.requests.agape import PaginacaoQuery
from acutis_api.communication.responses.agape import (
    ListarMembrosFamiliaAgapeResponsePaginada,
    MembroFamiliaAgapeResponse,
)
from acutis_api.domain.repositories.agape import AgapeRepositoryInterface
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
        self, familia_id: uuid.UUID
    ) -> ListarMembrosFamiliaAgapeResponsePaginada:
        filtros: PaginacaoQuery = PaginacaoQuery.parse_obj(request.args)

        familia = self.__repository.buscar_familia_por_id(familia_id)

        if familia is None:
            raise HttpNotFoundError('Família não encontrada.')

        instancias = self.__repository.listar_membros_familia(
            familia_id=familia_id
        )

        membros, total = self.__repository.query_paginada(
            instancias, filtros.pagina, filtros.por_pagina
        )

        return ListarMembrosFamiliaAgapeResponsePaginada(
            pagina=filtros.pagina,
            paginas=math.ceil(total / filtros.por_pagina),
            total=total,
            resultados=[
                MembroFamiliaAgapeResponse(
                    id=membro.id,
                    cpf=membro.cpf,
                    nome=membro.nome,
                    email=membro.email,
                    telefone=membro.telefone,
                    ocupacao=membro.ocupacao,
                    renda=membro.renda,
                    responsavel=membro.responsavel,
                    idade=calcular_idade(membro.data_nascimento),
                ).model_dump()
                for membro in membros
            ],
        )
