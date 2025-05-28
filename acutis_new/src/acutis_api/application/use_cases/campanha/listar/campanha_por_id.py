import uuid

from acutis_api.communication.responses.campanha import (
    CampanhaCompletaResponse,
    CampanhaResponse,
    CampoAdicionalResponse,
    LandingPageResponse,
)
from acutis_api.domain.repositories.campanha import CampanhaRepositoryInterface
from acutis_api.domain.services.file_service import FileServiceInterface
from acutis_api.exception.errors.not_found import HttpNotFoundError


class BuscaCampanhaPorIdUseCase:
    def __init__(
        self,
        repository: CampanhaRepositoryInterface,
        s3_service: FileServiceInterface,
    ):
        self.__repository = repository
        self.__s3_service = s3_service

    def execute(self, fk_campanha_id: uuid.UUID):
        busca_campanha_por_id = self.__repository.buscar_campanha_por_id(
            fk_campanha_id
        )

        if busca_campanha_por_id is None:
            raise HttpNotFoundError('Campanha não encontrada')

        campanha, landing_page = busca_campanha_por_id
        campos_adicionais = self.__repository.buscar_campos_adicionais(
            fk_campanha_id
        )

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

        campos_adicionais_response = []
        if campos_adicionais is not None:
            for campo in campos_adicionais:
                campos_adicionais_response.append(
                    CampoAdicionalResponse(
                        id=campo.id,
                        nome_campo=campo.nome_campo,
                        tipo_campo=campo.tipo_campo,
                        obrigatorio=campo.obrigatorio,
                    )
                )

        landing_page_response = None
        if campanha.landing_page:
            landing_page_response = LandingPageResponse(
                id=landing_page.id,
            )

        return CampanhaCompletaResponse(
            campanha=campanha_response,
            campos_adicionais=campos_adicionais_response,
            landing_page=landing_page_response,
        ).model_dump()
