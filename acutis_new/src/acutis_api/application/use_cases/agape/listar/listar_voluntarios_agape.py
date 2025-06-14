import math

from flask import request

from acutis_api.communication.enums.membros import PerfilEnum
from acutis_api.communication.requests.agape import PaginacaoQuery
from acutis_api.communication.responses.agape import (
    ListarVoluntariosAgapeResponse,
    VoluntarioAgapeResponse,
)
from acutis_api.domain.repositories.agape import AgapeRepositoryInterface


class ListarVoluntariosAgapeUseCase:
    def __init__(self, agape_repository: AgapeRepositoryInterface):
        self.agape_repository = agape_repository

    def execute(self) -> ListarVoluntariosAgapeResponse:
        filtros: PaginacaoQuery = PaginacaoQuery.parse_obj(request.args)

        membros_agape_query = self.agape_repository.listar_voluntarios_agape()

        membros_agape, total = self.agape_repository.query_paginada(
            membros_agape_query,
            filtros.pagina,
            filtros.por_pagina,
        )

        voluntarios_response = [
            VoluntarioAgapeResponse(
                id=membro.id,
                nome=membro.nome,
                email=membro.email,
                telefone=membro.telefone,
                perfil=PerfilEnum.voluntario_agape.value,
            )
            for membro in membros_agape
        ]

        return ListarVoluntariosAgapeResponse(
            pagina=filtros.pagina,
            paginas=math.ceil(total / filtros.por_pagina),
            total=total,
            resultados=voluntarios_response,
        )
