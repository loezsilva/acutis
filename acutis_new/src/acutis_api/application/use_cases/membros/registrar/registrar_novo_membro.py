import secrets

from flask import session

from acutis_api.application.utils.funcoes_auxiliares import (
    TokenSaltEnum,
    gerar_token,
)
from acutis_api.communication.requests.membros import (
    RegistrarNovoMembroFormData,
)
from acutis_api.communication.responses.membros import (
    RegistrarNovoMembroResponse,
)
from acutis_api.domain.repositories.membros import (
    MembrosRepositoryInterface,
)
from acutis_api.domain.repositories.schemas.membros import (
    RegistrarNovoEnderecoSchema,
    RegistrarNovoLeadSchema,
    RegistrarNovoMembroSchema,
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
from acutis_api.exception.errors.not_found import HttpNotFoundError
from acutis_api.exception.errors.unprocessable_entity import (
    HttpUnprocessableEntityError,
)


class RegistrarNovoMembroUseCase:
    def __init__(
        self,
        repository: MembrosRepositoryInterface,
        file_service: FileServiceInterface,
        notification: EnviarNotificacaoInterface,
    ):
        self._repository = repository
        self._file_service = file_service
        self._notification = notification

    def execute(self, request: RegistrarNovoMembroFormData):
        db_membro = self._repository.verificar_cadastro_por_documento_e_email(
            request.membro.numero_documento, request.membro.email
        )
        if db_membro:
            if db_membro.numero_documento == request.membro.numero_documento:
                raise HttpConflictError('Número documento já cadastrado.')
            elif db_membro.email == request.membro.email:
                raise HttpConflictError('Email já cadastrado.')

        autenticacao_google = session.pop('google_auth', False)
        dados_lead = RegistrarNovoLeadSchema(
            nome=request.membro.nome,
            email=request.membro.email,
            telefone=request.membro.telefone,
            pais=request.endereco.pais,
            origem_cadastro=request.membro.origem_cadastro,
            senha=secrets.token_hex(16),
            status=autenticacao_google,
        )
        lead = self._repository.registrar_novo_lead(dados_lead)

        if request.campanha_id:
            campanha = self._repository.buscar_campanha_por_id(
                request.campanha_id
            )
            if not campanha:
                raise HttpNotFoundError('Ops, Campanha não encontrada.')
            if not campanha.ativa:
                raise HttpUnprocessableEntityError(
                    'Ops, a campanha está inativa e não pode receber cadastros.'  # noqa
                )
            self._repository.vincular_lead_a_campanha_registro(
                lead.id, campanha.id
            )

        dados_endereco = RegistrarNovoEnderecoSchema.model_validate(
            request.endereco.model_dump()
        )
        endereco = self._repository.registrar_novo_endereco(dados_endereco)

        foto = (
            self._file_service.salvar_arquivo(request.foto)
            if request.foto
            else None
        )
        dados_membro = RegistrarNovoMembroSchema(
            nome_social=request.membro.nome_social,
            data_nascimento=request.membro.data_nascimento,
            numero_documento=request.membro.numero_documento,
            sexo=request.membro.sexo,
            foto=foto,
            endereco_id=endereco.id,
            lead_id=lead.id,
        )
        self._repository.registrar_novo_membro(dados_membro)

        if not autenticacao_google:
            payload = {'email': request.membro.email}
            token = gerar_token(payload, TokenSaltEnum.ativar_conta)
            conteudo = ativar_conta_email_template(request.membro.nome, token)
            self._notification.enviar_email(
                request.membro.email, AssuntosEmailEnum.verificacao, conteudo
            )

        self._repository.salvar_alteracoes()

        response = RegistrarNovoMembroResponse.model_validate(
            lead
        ).model_dump()
        return response
