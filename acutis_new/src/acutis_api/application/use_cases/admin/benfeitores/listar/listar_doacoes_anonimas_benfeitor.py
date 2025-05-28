import math
import uuid

from acutis_api.communication.responses.admin_benfeitores import (
    ListarDoacoesAnonimasBenfeitorResponse,
    ListarDoacoesAnonimasBenfeitorSchema,
)
from acutis_api.domain.repositories.admin_benfeitores import (
    AdminBenfeitoresRepositoryInterface,
)
from acutis_api.domain.repositories.schemas.paginacao import PaginacaoQuery


class ListarDoacoesAnonimasBenfeitorUseCase:
    def __init__(self, repository: AdminBenfeitoresRepositoryInterface):
        self._repository = repository

    def execute(self, filtros: PaginacaoQuery, benfeitor_id: uuid.UUID):
        doacoes_anonimas, total = (
            self._repository.listar_doacoes_anonimas_benfeitor_pelo_id(
                filtros, benfeitor_id
            )
        )

        response = ListarDoacoesAnonimasBenfeitorResponse(
            pagina=filtros.pagina,
            paginas=math.ceil(total / filtros.por_pagina),
            total=total,
            doacoes=[
                ListarDoacoesAnonimasBenfeitorSchema(
                    data=doacao.criado_em,
                    hora=doacao.criado_em,
                    valor=doacao.valor,
                )
                for doacao in doacoes_anonimas
            ],
        ).model_dump()

        return response
