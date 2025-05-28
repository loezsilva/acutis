import math

from acutis_api.communication.responses.admin_benfeitores import (
    ListarBenfeitoresResponse,
    ListarBenfeitoresSchema,
)
from acutis_api.domain.repositories.admin_benfeitores import (
    AdminBenfeitoresRepositoryInterface,
)
from acutis_api.domain.repositories.schemas.admin_benfeitores import (
    ListarBenfeitoresFiltros,
)


class ListarBenfeitoresUseCase:
    def __init__(self, repository: AdminBenfeitoresRepositoryInterface):
        self._repository = repository

    def execute(self, filtros: ListarBenfeitoresFiltros):
        benfeitores, total = self._repository.listar_benfeitores(filtros)

        response = ListarBenfeitoresResponse(
            pagina=filtros.pagina,
            paginas=math.ceil(total / filtros.por_pagina),
            total=total,
            benfeitores=[
                ListarBenfeitoresSchema.model_validate(benfeitor)
                for benfeitor in benfeitores
            ],
        )

        return response
