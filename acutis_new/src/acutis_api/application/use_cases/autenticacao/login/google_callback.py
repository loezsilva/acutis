from datetime import timedelta

from flask import make_response, redirect, session
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
from acutis_api.communication.schemas.autenticacao import GoogleCallbackSchema
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


class GoogleCallbackUseCase:
    def __init__(
        self,
        google,
        repository: AutenticacaoRepositoryInterface,
        notification: EnviarNotificacaoInterface,
    ):
        self._google = google
        self._repository = repository
        self.__notification = notification

    def execute(self):
        token = self._google.authorize_access_token()
        dados_google = GoogleCallbackSchema.model_validate(token['userinfo'])
        response = make_response(redirect(session.pop('original_url')))

        lead = self._repository.buscar_lead_por_email(dados_google.email)
        if lead:
            if not lead.status:
                payload = {'email': lead.email}
                token = gerar_token(payload, TokenSaltEnum.ativar_conta)
                conteudo = ativar_conta_email_template(lead.nome, token)
                self.__notification.enviar_email(
                    lead.email, AssuntosEmailEnum.verificacao, conteudo
                )
                raise HttpForbiddenError(
                    'Ative sua conta pelo link enviado ao seu e-mail antes de fazer login.'  # noqa
                )

            access_token = create_access_token(identity=lead.id)
            refresh_token = create_refresh_token(identity=lead.id)

            set_access_cookies(response, access_token)
            set_refresh_cookies(response, refresh_token)
        else:
            response.set_cookie(
                key='email',
                value=dados_google.email,
                max_age=timedelta(seconds=60),
                secure=True,
                samesite='None',
                httponly=False,
            )
            response.set_cookie(
                key='nome',
                value=dados_google.name,
                max_age=timedelta(seconds=60),
                secure=True,
                samesite='None',
                httponly=False,
            )

        return response
