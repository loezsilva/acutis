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
                fk_cargo_oficial_id=campanha.fk_cargo_oficial_id,
            )

            landing_page_response = None
            if campanha.landing_page:
                landing_page_response = LandingPageResponse(
                    id=campanha.landing_page.id,
                )

            campanha_completa = CampanhaCompletaResponse(
                campanha=campanha_response,
                landing_page=landing_page_response,
                campos_adicionais=[],
            )

            campanhas_completas.append(campanha_completa)

        return ListagemCompletaDeCampanhaResponse(
            campanhas=campanhas_completas,
            pagina=resultado_paginado.page,
            total=resultado_paginado.total,
            paginas=resultado_paginado.pages,
            por_pagina=resultado_paginado.per_page,
        ).model_dump()
