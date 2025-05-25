from acutis_api.application.utils.funcoes_auxiliares import (
    TokenSaltEnum,
    gerar_token,
)
from acutis_api.communication.requests.autenticacao import (
    RecuperarSenhaRequest,
)
from acutis_api.domain.repositories.autenticacao import (
    AutenticacaoRepositoryInterface,
)
from acutis_api.domain.services.enviar_notificacao import (
    AssuntosEmailEnum,
    EnviarNotificacaoInterface,
)
from acutis_api.domain.templates.email_templates import (
    reset_password_email_template,
)
from acutis_api.exception.errors.not_found import HttpNotFoundError


class RecuperarSenhaUseCase:
    def __init__(
        self,
        autenticacao_repository: AutenticacaoRepositoryInterface,
        notificacao: EnviarNotificacaoInterface,
    ):
        self.__autenticacao_repository = autenticacao_repository
        self.__notificacao = notificacao

    def execute(self, request: RecuperarSenhaRequest):
        email = request.email.strip()
        url_redirect = request.url_redirecionamento.strip()

        usuario = self.__autenticacao_repository.buscar_lead_por_email(email)
        if usuario is None:
            raise HttpNotFoundError(
                'Lamentamos que não foi possível identificá-lo'
                'segundo as informações fornecidas.'
            )
        payload = {'email': email}
        token = gerar_token(payload, salt=TokenSaltEnum.recuperar_senha)
        html = reset_password_email_template(usuario.nome, token, url_redirect)

        self.__notificacao.enviar_email(
            email, AssuntosEmailEnum.recuperar_senha, html
        )
