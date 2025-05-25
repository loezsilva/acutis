from pydantic import EmailStr

from acutis_api.application.utils.funcoes_auxiliares import (
    TokenSaltEnum,
    gerar_token,
)
from acutis_api.domain.repositories.membros import MembrosRepositoryInterface
from acutis_api.domain.services.enviar_notificacao import (
    AssuntosEmailEnum,
    EnviarNotificacaoInterface,
)
from acutis_api.domain.templates.email_templates import (
    ativar_conta_email_template,
)
from acutis_api.exception.errors.forbidden import HttpForbiddenError
from acutis_api.exception.errors.not_found import HttpNotFoundError


class BuscaCadastroPorEmail:
    def __init__(
        self,
        repository: MembrosRepositoryInterface,
        notification: EnviarNotificacaoInterface,
    ):
        self.__repository = repository
        self.__notification = notification

    def execute(self, email: EmailStr):
        lead = self.__repository.buscar_lead_por_email(email)
        if not lead:
            raise HttpNotFoundError('Cadastro não encontrado.')

        if not lead.status:
            payload = {'email': email}
            token = gerar_token(payload, TokenSaltEnum.ativar_conta)
            conteudo = ativar_conta_email_template(lead.nome, token)
            self.__notification.enviar_email(
                email, AssuntosEmailEnum.verificacao, conteudo
            )
            raise HttpForbiddenError(
                'Ative sua conta pelo link enviado ao seu e-mail antes de fazer login.'  # noqa
            )
