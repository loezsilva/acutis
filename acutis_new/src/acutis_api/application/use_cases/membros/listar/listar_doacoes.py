import math

from acutis_api.communication.requests.paginacao import PaginacaoQuery
from acutis_api.communication.responses.membros import (
    DoacaoMembroBenfeitorSchema,
    DoacoesMembroBenfeitorResponse,
)
from acutis_api.domain.entities.lead import Lead
from acutis_api.domain.repositories.membros import MembrosRepositoryInterface
from acutis_api.domain.services.file_service import FileServiceInterface
from acutis_api.exception.errors.not_found import HttpNotFoundError


class ListarDoacoesUseCase:
    def __init__(
        self,
        repository: MembrosRepositoryInterface,
        file_service: FileServiceInterface,
    ):
        self._repository = repository
        self._file_service = file_service

    def execute(self, filtros: PaginacaoQuery, usuario_logado: Lead):
        if (
            not usuario_logado.membro
            or not usuario_logado.membro.fk_benfeitor_id
        ):
            raise HttpNotFoundError('Nenhuma doação encontrada.')

        doacoes, total = self._repository.listar_doacoes(
            filtros, usuario_logado.membro.fk_benfeitor_id
        )

        response = DoacoesMembroBenfeitorResponse(
            total=total,
            pagina=filtros.pagina,
            paginas=math.ceil(total / filtros.por_pagina),
            doacoes=[
                DoacaoMembroBenfeitorSchema(
                    doacao_id=doacao.doacao_id,
                    nome_campanha=doacao.nome_campanha,
                    foto_campanha=self._file_service.buscar_url_arquivo(
                        doacao.foto_campanha
                    )
                    if doacao.foto_campanha
                    else None,
                    tipo_doacao=doacao.tipo_doacao,
                )
                for doacao in doacoes
            ],
        )

        return response
