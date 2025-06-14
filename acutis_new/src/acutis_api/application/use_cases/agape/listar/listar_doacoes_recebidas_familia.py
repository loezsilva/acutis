import math
from uuid import UUID

from flask import request

from acutis_api.communication.requests.agape import PaginacaoQuery
from acutis_api.communication.responses.agape import (
    DoacaoRecebidaDetalheSchema,
    ListarDoacoesRecebidasFamiliaResponse,
)
from acutis_api.domain.repositories.agape import AgapeRepositoryInterface
from acutis_api.domain.services.file_service import FileServiceInterface
from acutis_api.exception.errors.not_found import HttpNotFoundError


class ListarDoacoesRecebidasFamiliaUseCase:
    def __init__(
        self,
        agape_repository: AgapeRepositoryInterface,
        file_service: FileServiceInterface,
    ):
        self._agape_repository = agape_repository
        self._file_service = file_service

    def execute(
        self, familia_id: UUID
    ) -> ListarDoacoesRecebidasFamiliaResponse:
        filtros: PaginacaoQuery = PaginacaoQuery.parse_obj(request.args)

        familia = self._agape_repository.buscar_familia_por_id(
            familia_id=familia_id
        )

        if familia is None:
            raise HttpNotFoundError('Família não encontrada')

        doacoes_query = self._agape_repository.listar_todos_os_recibos_doacoes(
            familia_id=familia_id
        )

        doacoes, total = self._agape_repository.query_paginada(
            doacoes_query,
            filtros.pagina,
            filtros.por_pagina,
        )

        doacoes_recebidas_respostas = []

        for doacao in doacoes:
            doacoes_recebidas_respostas.append(
                DoacaoRecebidaDetalheSchema(
                    nome_acao=doacao.nome_acao,
                    doacao_id=doacao.doacao_id,
                    ciclo_acao_id=doacao.ciclo_acao_id,
                    dia_horario=doacao.dia_horario,
                    recibos=doacao.recibos if doacao.recibos else [],
                )
            )

        return ListarDoacoesRecebidasFamiliaResponse(
            pagina=filtros.pagina,
            paginas=math.ceil(total / filtros.por_pagina),
            total=total,
            resultados=doacoes_recebidas_respostas,
        ).model_dump()
