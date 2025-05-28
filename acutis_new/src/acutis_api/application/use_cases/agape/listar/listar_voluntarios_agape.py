import math

from acutis_api.communication.enums.membros import PerfilEnum
from acutis_api.communication.responses.agape import (
    ListarVoluntariosAgapeResponse,
    VoluntarioAgapeResponse,
)
from acutis_api.domain.repositories.agape import AgapeRepositoryInterface
from acutis_api.domain.repositories.schemas.agape import PaginacaoSchema


class ListarVoluntariosAgapeUseCase:
    def __init__(self, agape_repository: AgapeRepositoryInterface):
        self.agape_repository = agape_repository

    def execute(
        self, filtros: PaginacaoSchema
    ) -> ListarVoluntariosAgapeResponse:
        membros_agape, total = self.agape_repository.listar_voluntarios_agape(
            filtros=filtros
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
