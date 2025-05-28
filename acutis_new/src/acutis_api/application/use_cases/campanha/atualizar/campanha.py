from acutis_api.communication.requests.campanha import (
    RegistrarCampanhaSchema,
    RegistrarNovaCampanhaFormData,
)
from acutis_api.communication.responses.campanha import (
    RegistrarNovaCampanhaResponse,
)
from acutis_api.domain.entities.campanha import Campanha, ObjetivosCampanhaEnum
from acutis_api.domain.repositories.campanha import CampanhaRepositoryInterface
from acutis_api.domain.services.file_service import FileServiceInterface
from acutis_api.domain.services.gateway_pagamento import (
    GatewayPagamentoInterface,
)
from acutis_api.exception.errors.bad_request import HttpBadRequestError
from acutis_api.exception.errors.conflict import HttpConflictError
from acutis_api.exception.errors.not_found import HttpNotFoundError


class AtualizarCampanhaUseCase:
    def __init__(
        self,
        campanha_repository: CampanhaRepositoryInterface,
        s3_service: FileServiceInterface,
        itau_api: GatewayPagamentoInterface,
    ):
        self.__campanha_repository = campanha_repository
        self.__s3_service = s3_service
        self._itau_api = itau_api

    def execute(  # NOSONAR
        self,
        dados_da_requisicao: RegistrarNovaCampanhaFormData,
        fk_campanha_id: int,
    ) -> dict:
        dados_da_campanha = dados_da_requisicao.dados_da_campanha
        foto_capa = dados_da_requisicao.foto_capa
        campos_adicionais = dados_da_requisicao.campos_adicionais
        campanha_id = fk_campanha_id

        buscar_campanha = self.__campanha_repository.buscar_campanha_por_id(
            campanha_id
        )

        if buscar_campanha is None:
            raise HttpNotFoundError('Campanha não encontrada')

        campanha_para_atualizar, landing_page_para_atualizar = buscar_campanha

        verifica_nome_campanha_ja_cadastrado = (
            self.__campanha_repository.verificar_nome_da_campanha(
                dados_da_campanha.nome
            )
        )

        if verifica_nome_campanha_ja_cadastrado is not None:
            if verifica_nome_campanha_ja_cadastrado.id != campanha_id:
                raise HttpConflictError('Nome de campanha já cadastrado')

        if foto_capa is not None:
            dados_da_campanha.foto_capa = self.__s3_service.salvar_arquivo(
                foto_capa
            )

        if dados_da_campanha.objetivo == ObjetivosCampanhaEnum.oficiais:
            if dados_da_campanha.fk_cargo_oficial_id is None:
                raise HttpBadRequestError(
                    'Deve ser informado um cargo oficial.'
                )

        campanha = self.__campanha_repository.atualizar_campanha(
            dados_da_campanha=dados_da_campanha,
            campanha_para_atualizar=campanha_para_atualizar,
        )

        if dados_da_campanha.objetivo == ObjetivosCampanhaEnum.doacao:
            self._atualizar_campanha_doacao(campanha, dados_da_campanha)

        campos_adicionais_da_campanha = (
            self.__campanha_repository.buscar_campos_adicionais(
                campanha_para_atualizar.id
            )
        )

        if campos_adicionais is not None:
            for campo_existente in campos_adicionais_da_campanha:
                campos_list = next(
                    (
                        campo
                        for campo in campos_adicionais
                        if campo.nome_campo == campo_existente.nome_campo
                    ),
                    None,
                )
                if campos_list:
                    self.__campanha_repository.atualizar_campos_adicionais(
                        campo_existente, campos_list
                    )

        self.__campanha_repository.salvar_alteracoes()

        response = RegistrarNovaCampanhaResponse.model_validate(
            campanha
        ).model_dump()

        return response

    def _atualizar_campanha_doacao(
        self, campanha: Campanha, dados_da_campanha: RegistrarCampanhaSchema
    ):
        if not dados_da_campanha.chave_pix:
            raise HttpBadRequestError(
                'A chave pix é obrigatória para campanhas com o objetivo de doação.'  # noqa
            )

        if campanha.campanha_doacao.chave_pix != dados_da_campanha.chave_pix:
            self._itau_api.deletar_chave_pix_webhook(campanha.chave_pix)
            self._itau_api.registrar_chave_pix_webhook(
                dados_da_campanha.chave_pix
            )

            self.__campanha_repository.atualizar_campanha_doacao(
                dados_da_campanha.chave_pix,
                campanha.campanha_doacao,
            )
