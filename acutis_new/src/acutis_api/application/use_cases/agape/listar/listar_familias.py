import math

from flask import request

from acutis_api.communication.requests.agape import PaginacaoQuery
from acutis_api.communication.responses.agape import (
    FamiliaAgapeResponse,
    ListarFamiliasAgapeResponsePaginada,
)
from acutis_api.domain.repositories.agape import AgapeRepositoryInterface
from acutis_api.domain.services.file_service import FileServiceInterface


class ListarFamiliasUseCase:
    """
    Caso de uso para listar as famílias cadastradas:
    """

    def __init__(
        self,
        agape_repository: AgapeRepositoryInterface,
        file_service: FileServiceInterface,
    ):
        self.__repository = agape_repository
        self.__file_service = file_service

    def execute(self) -> ListarFamiliasAgapeResponsePaginada:
        filtros: PaginacaoQuery = PaginacaoQuery.parse_obj(request.args)

        familias, total = self.__repository.listar_familias(filtros)

        # Cria resposta paginada
        pagina_atual = filtros.pagina

        familias_respostas = []
        for familia in familias:
            fotos_familia = self._agape_repository.listar_fotos_por_familia_id(
                familia.id
            )
            fotos_urls = [
                self.__file_service.buscar_url_arquivo(foto.foto)
                for foto in fotos_familia
                if foto.foto
            ]
            familias_respostas.append(
                FamiliaAgapeResponse(
                    id=familia.id,
                    nome_familia=familia.nome_familia,
                    criado_em=familia.criado_em,
                    cadastrada_por=familia.cadastrada_por,
                    endereco_id=familia.fk_endereco_id,
                    observacao=familia.observacao,
                    comprovante_residencia=(
                        familia.comprovante_residencia
                        if familia.comprovante_residencia
                        else None
                    ),
                    fotos_familia_urls=fotos_urls,
                ).model_dump()
            )

        return ListarFamiliasAgapeResponsePaginada(
            pagina=pagina_atual,
            paginas=math.ceil(total / filtros.por_pagina),
            total=total,
            resultados=familias_respostas,
        )
