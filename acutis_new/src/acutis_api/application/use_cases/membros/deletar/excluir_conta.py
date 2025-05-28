from flask_jwt_extended import current_user

from acutis_api.application.utils.funcoes_auxiliares import (
    TokenSaltEnum,
    gerar_token,
)
from acutis_api.domain.services.enviar_notificacao import (
    AssuntosEmailEnum,
    EnviarNotificacaoInterface,
)
from acutis_api.domain.templates.email_templates import (
    excluir_conta_email_template,
)


class ExcluirContaUseCase:
    def __init__(self, notification: EnviarNotificacaoInterface):
        self.__notification = notification

    def execute(self) -> None:
        payload = {
            'email': current_user.email,
            'fk_lead_id': str(current_user.id),
        }
        token = gerar_token(payload, TokenSaltEnum.excluir_conta)

        conteudo = excluir_conta_email_template(current_user.nome, token)
        self.__notification.enviar_email(
            current_user.email, AssuntosEmailEnum.excluir_conta, conteudo
        )
