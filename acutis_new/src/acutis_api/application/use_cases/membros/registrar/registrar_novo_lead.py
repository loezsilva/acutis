import secrets
import uuid

from flask import session

from acutis_api.application.use_cases.base_classes import (
    CamposAdicionaisValidators,
)
from acutis_api.application.utils.funcoes_auxiliares import (
    TokenSaltEnum,
    decodificar_base64_para_arquivo,
    gerar_token,
)
from acutis_api.communication.requests.membros import (
    CampoAdicionalSchema,
    RegistrarNovoLeadRequest,
)
from acutis_api.communication.responses.membros import (
    RegistrarNovoLeadResponse,
)
from acutis_api.domain.entities.campanha import Campanha
from acutis_api.domain.entities.campo_adicional import (
    CampoAdicional,
)
from acutis_api.domain.entities.lead import Lead
from acutis_api.domain.repositories.membros import MembrosRepositoryInterface
from acutis_api.domain.repositories.schemas.membros import (
    RegistrarNovoLeadSchema,
)
from acutis_api.domain.services.enviar_notificacao import (
    AssuntosEmailEnum,
    EnviarNotificacaoInterface,
)
from acutis_api.domain.services.file_service import FileServiceInterface
from acutis_api.domain.templates.email_templates import (
    ativar_conta_email_template,
)
from acutis_api.exception.errors.conflict import HttpConflictError


class RegistrarNovoLeadUseCase:
    def __init__(
        self,
        repository: MembrosRepositoryInterface,
        file_service: FileServiceInterface,
        notification: EnviarNotificacaoInterface,
    ):
        self._repository = repository
        self._file_service = file_service
        self._notification = notification
        self._validator = CamposAdicionaisValidators()

    def execute(self, request: RegistrarNovoLeadRequest):
        autenticacao_google = session.pop('google_auth', False)
        lead = self._buscar_ou_registrar_lead(
            request, autenticacao_google, secrets.token_hex(16)
        )

        if request.campanha_id:
            campanha = self._buscar_e_validar_campanha(request.campanha_id)
            self._repository.vincular_lead_a_campanha_registro(
                lead.id, campanha.id
            )

            if campanha.campos_adicionais:
                self._processar_campos_adicionais(
                    lead.id,
                    request.campos_adicionais,
                    campanha.campos_adicionais,
                )

        if not autenticacao_google:
            payload = {'email': request.email}
            token = gerar_token(payload, TokenSaltEnum.ativar_conta)
            conteudo = ativar_conta_email_template(request.nome, token)
            self._notification.enviar_email(
                request.email, AssuntosEmailEnum.verificacao, conteudo
            )
        self._repository.salvar_alteracoes()

        response = RegistrarNovoLeadResponse.model_validate(lead).model_dump()
        return response

    def _buscar_e_validar_campanha(self, campanha_id: uuid.UUID) -> Campanha:
        campanha = self._repository.buscar_campanha_por_id(campanha_id)
        self._validator.verificar_campanha_valida(campanha)
        return campanha

    def _buscar_ou_registrar_lead(
        self,
        request: RegistrarNovoLeadRequest,
        autenticacao_google: bool,
        senha_aleatoria: str,
    ) -> Lead:
        lead = self._repository.buscar_lead_por_email(request.email)
        if lead:
            raise HttpConflictError('Ops, email já cadastrado.')

        dados_lead = RegistrarNovoLeadSchema(
            nome=request.nome,
            email=request.email,
            telefone=request.telefone,
            pais=request.pais,
            origem_cadastro=request.origem_cadastro,
            senha=senha_aleatoria,
            status=autenticacao_google,
        )
        lead = self._repository.registrar_novo_lead(dados_lead)
        return lead

    def _processar_campos_adicionais(
        self,
        lead_id: uuid.UUID,
        campos_recebidos: list[CampoAdicionalSchema],
        campos_campanha: list[CampoAdicional],
    ):
        self._validator.validar_campos_adicionais(
            campos_recebidos, campos_campanha
        )

        for campo in campos_recebidos:
            campo.valor_campo = (
                self._processar_e_salvar_arquivo_base64(campo.valor_campo)
                if 'data:' in campo.valor_campo
                else campo.valor_campo
            )

            self._repository.registrar_campo_adicional_metadado_lead(
                lead_id, campo
            )

    def _processar_e_salvar_arquivo_base64(self, base64: str) -> str:
        arquivo, nome_arquivo = decodificar_base64_para_arquivo(base64)
        return self._file_service.salvar_arquivo(arquivo, nome_arquivo)
