from acutis_api.communication.responses.campanha import (
    CampanhaCompletaResponse,
    CampanhaResponse,
    LandingPageResponse,
    ListagemCompletaDeCampanhaResponse,
)
from acutis_api.domain.repositories.campanha import CampanhaRepositoryInterface
from acutis_api.domain.services.file_service import FileServiceInterface


class ListarCampanhasUseCase:
    def __init__(
        self,
        s3_service: FileServiceInterface,
        campanha_repository: CampanhaRepositoryInterface,
    ):
        self.__campanha_repository = campanha_repository
        self.__s3_service = s3_service

    def execute(
        self, filtros_da_requisicao
    ) -> ListagemCompletaDeCampanhaResponse:
        resultado_paginado = self.__campanha_repository.listar_campanhas(
            filtros_da_requisicao
        )

        campanhas_completas = []

        for campanha in resultado_paginado.items:
            campanha_response = CampanhaResponse(
                id=campanha.id,
                objetivo=campanha.objetivo,
                nome=campanha.nome,
                publica=campanha.publica,
                ativa=campanha.ativa,
                meta=campanha.meta,
                capa=self.__s3_service.buscar_url_arquivo(campanha.capa)
                if campanha.capa is not None
                else None,
                chave_pix=campanha.chave_pix,
                criado_em=campanha.criado_em,
                criado_por=campanha.criado_por,
                atualizado_em=campanha.atualizado_em,
            )

            landing_page_response = None
            if campanha.landing_page:
                landing_page_response = LandingPageResponse(
                    id=campanha.landing_page.id,
                    fk_campanha_id=campanha.landing_page.fk_campanha_id,
                    conteudo=campanha.landing_page.conteudo,
                    shlink=campanha.landing_page.shlink,
                    criado_em=campanha.landing_page.criado_em,
                    atualizado_em=campanha.landing_page.atualizado_em,
                )

            campanha_completa = CampanhaCompletaResponse(
                campanha=campanha_response,
                landing_page=landing_page_response,
            )

            campanhas_completas.append(campanha_completa)

        return ListagemCompletaDeCampanhaResponse(
            campanhas=campanhas_completas,
            pagina=resultado_paginado.page,
            total=resultado_paginado.total,
            paginas=resultado_paginado.pages,
            por_pagina=resultado_paginado.per_page,
        )
