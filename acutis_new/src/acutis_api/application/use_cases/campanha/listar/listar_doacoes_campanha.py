import math
import uuid

from acutis_api.communication.responses.campanha import (
    ListarDoacoesCampanhaResponse,
    ListarDoacoesCampanhaSchema,
)
from acutis_api.domain.repositories.campanha import CampanhaRepositoryInterface
from acutis_api.domain.repositories.schemas.paginacao import PaginacaoQuery


class ListarDoacoesCampanhaUseCase:
    def __init__(self, repository: CampanhaRepositoryInterface):
        self._repository = repository

    def execute(self, filtros: PaginacaoQuery, campanha_id: uuid.UUID):
        doacoes, total = self._repository.listar_doacoes_campanha_pelo_id(
            filtros, campanha_id
        )

        response = ListarDoacoesCampanhaResponse(
            pagina=filtros.pagina,
            paginas=math.ceil(total / filtros.por_pagina),
            total=total,
            doacoes=[
                ListarDoacoesCampanhaSchema.model_validate(doacao)
                for doacao in doacoes
            ],
        ).model_dump()

        return response
