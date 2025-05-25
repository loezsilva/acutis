from http import HTTPStatus

from acutis_api.communication.requests.campanha import (
    RegistrarNovaCampanhaFormData,
)
from acutis_api.communication.responses.campanha import (
    RegistrarNovaCampanhaResponse,
)
from acutis_api.domain.entities.campanha import ObjetivosCampanhaEnum
from acutis_api.domain.repositories.campanha import CampanhaRepositoryInterface
from acutis_api.domain.services.file_service import FileServiceInterface
from acutis_api.domain.services.gateway_pagamento import (
    GatewayPagamentoInterface,
)
from acutis_api.exception.errors.bad_request import HttpBadRequestError
from acutis_api.exception.errors.conflict import HttpConflictError


class RegistrarCampanhaUseCase:
    def __init__(
        self,
        campanha_repository: CampanhaRepositoryInterface,
        s3_service: FileServiceInterface,
        payment_service: GatewayPagamentoInterface,
    ):
        self.__campanha_repository = campanha_repository
        self.__s3_service = s3_service

    def execute(
        self, dados_da_requisicao: RegistrarNovaCampanhaFormData
    ) -> tuple[dict, HTTPStatus]:
        dados_da_campanha = dados_da_requisicao.dados_da_campanha
        dados_da_landing_page = dados_da_requisicao.dados_da_landing_page
        foto_capa = dados_da_requisicao.foto_capa
        campos_adicionais = dados_da_requisicao.campos_adicionais

        verifica_nome_campanha_ja_cadastrado = (
            self.__campanha_repository.verificar_nome_da_campanha(
                dados_da_campanha.nome
            )
        )
        if verifica_nome_campanha_ja_cadastrado is not None:
            raise HttpConflictError('Nome de campanha já cadastrado')

        if foto_capa is not None:
            foto_capa_salva_no_bucket = self.__s3_service.salvar_arquivo(
                foto_capa
            )
            dados_da_campanha.foto_capa = foto_capa_salva_no_bucket

        # adicionar tratamento de iformações bancárias caso campanha de doação

        if dados_da_campanha.objetivo in {
            ObjetivosCampanhaEnum.cadastro,
            ObjetivosCampanhaEnum.pre_cadastro,
            ObjetivosCampanhaEnum.oficiais,
        }:
            if dados_da_landing_page is None or (
                dados_da_landing_page.conteudo is None
            ):
                raise HttpBadRequestError(
                    'É necessário informar o conteúdo da landing page'
                )

            if dados_da_campanha.objetivo == ObjetivosCampanhaEnum.oficiais:
                if dados_da_campanha.fk_cargo_oficial_id is None:
                    raise HttpBadRequestError(
                        'Deve ser informado um cargo oficial.'
                    )

        campanha = self.__campanha_repository.registrar_nova_campanha(
            dados_da_campanha=dados_da_campanha
        )

        if dados_da_landing_page is not None:
            self.__campanha_repository.criar_landing_page(
                campanha.id, dados_da_landing_page
            )

        if campos_adicionais is not None:
            self.__campanha_repository.criar_campos_adicionais(
                campanha.id, campos_adicionais
            )

        self.__campanha_repository.salvar_alteracoes()

        response = RegistrarNovaCampanhaResponse.model_validate(
            campanha
        ).model_dump()

        return response
