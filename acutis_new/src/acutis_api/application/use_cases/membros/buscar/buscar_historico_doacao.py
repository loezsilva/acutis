import math
import uuid

from acutis_api.communication.requests.paginacao import PaginacaoQuery
from acutis_api.communication.responses.membros import (
    HistoricoDoacaoResponse,
    HistoricoDoacaoSchema,
)
from acutis_api.domain.entities.lead import Lead
from acutis_api.domain.repositories.membros import MembrosRepositoryInterface
from acutis_api.exception.errors.forbidden import HttpForbiddenError
from acutis_api.exception.errors.not_found import HttpNotFoundError


class BuscarHistoricoDoacaoUseCase:
    def __init__(self, repository: MembrosRepositoryInterface):
        self._repository = repository

    def execute(
        self,
        filtros: PaginacaoQuery,
        usuario_logado: Lead,
        doacao_id: uuid.UUID,
    ):
        doacao = self._repository.buscar_doacao_por_id(doacao_id)
        if not doacao:
            raise HttpNotFoundError('Doação não encontrada.')

        if (
            not usuario_logado.membro
            or not usuario_logado.membro.fk_benfeitor_id
            or usuario_logado.membro.fk_benfeitor_id != doacao.fk_benfeitor_id
        ):
            raise HttpForbiddenError(
                'Você não tem permissão para visualizar essa doação.'
            )

        historico_doacoes, total = (
            self._repository.buscar_historico_doacao_por_doacao_id(
                filtros,
                doacao.id,
            )
        )

        response = HistoricoDoacaoResponse(
            pagina=filtros.pagina,
            paginas=math.ceil(total / filtros.por_pagina),
            total=total,
            historico_doacao=[
                HistoricoDoacaoSchema.model_validate(doacao).model_dump()
                for doacao in historico_doacoes
            ],
        ).model_dump()

        return response
