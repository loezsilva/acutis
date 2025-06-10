from flask import jsonify, make_response
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    set_access_cookies,
    set_refresh_cookies,
)

from acutis_api.application.utils.funcoes_auxiliares import (
    TokenSaltEnum,
    gerar_token,
)
from acutis_api.communication.requests.autenticacao import (
    LoginRequest,
    UsarHttpOnlyQuery,
)
from acutis_api.domain.repositories.autenticacao import (
    AutenticacaoRepositoryInterface,
)
from acutis_api.domain.services.enviar_notificacao import (
    AssuntosEmailEnum,
    EnviarNotificacaoInterface,
)
from acutis_api.domain.templates.email_templates import (
    ativar_conta_email_template,
)
from acutis_api.exception.errors.forbidden import HttpForbiddenError
from acutis_api.exception.errors.not_found import HttpNotFoundError
from acutis_api.infrastructure.settings import settings


class LoginUseCase:
    def __init__(
        self,
        repository: AutenticacaoRepositoryInterface,
        notification: EnviarNotificacaoInterface,
    ):
        self._repository = repository
        self._notification = notification

    def execute(self, request: LoginRequest, query: UsarHttpOnlyQuery):
        lead = self._repository.buscar_lead_por_email(request.email)
        if not lead:
            raise HttpNotFoundError('Ops, email ou senha incorretos.')

        if settings.ENVIRONMENT != 'development' and not lead.status:
            payload = {'email': request.email}
            token = gerar_token(payload, TokenSaltEnum.ativar_conta)
            conteudo = ativar_conta_email_template(lead.nome, token)
            self._notification.enviar_email(
                request.email, AssuntosEmailEnum.verificacao, conteudo
            )
            raise HttpForbiddenError(
                'Ative sua conta pelo link enviado ao seu e-mail antes de fazer login.'  # noqa
            )

        if not lead.verificar_senha(request.senha.get_secret_value()):
            raise HttpNotFoundError('Ops, email ou senha incorretos.')

        self._repository.atualizar_data_ultimo_acesso(lead)
        self._repository.salvar_alteracoes()

        access_token = create_access_token(identity=lead.id)
        refresh_token = create_refresh_token(identity=lead.id)

        if query.httponly:
            response = make_response()
            set_access_cookies(response, access_token)
            set_refresh_cookies(response, refresh_token)

        else:
            response = jsonify({
                'access_token': access_token,
                'refresh_token': refresh_token,
            })

        return response
