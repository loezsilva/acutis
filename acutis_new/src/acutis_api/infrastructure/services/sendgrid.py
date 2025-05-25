from http import HTTPStatus

from httpx import Response
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from acutis_api.domain.services.enviar_notificacao import (
    EnviarNotificacaoInterface,
)
from acutis_api.infrastructure.settings import settings


class SendGridService(EnviarNotificacaoInterface):
    def enviar_email(
        self, destinatario: str, assunto: str, conteudo: str
    ) -> Response | None:
        if settings.ENVIRONMENT != 'producao':
            if settings.ENVIRONMENT == 'teste':
                return None
            destinatario = 'emaildev50@gmail.com'  # pragma: no cover

        email = Mail(
            from_email=settings.SENDGRID_EMAIL,
            to_emails=destinatario,
            subject=assunto,
            html_content=conteudo,
        )

        sendgrid = SendGridAPIClient(  # pragma: no cover
            settings.SENDGRID_API_KEY
        )
        response: Response = sendgrid.send(email)  # pragma: no cover
        if not HTTPStatus(response.status_code).is_success:  # pragma: no cover
            raise Exception(  # NOSONAR
                f'Ocorreu um erro ao enviar o email. {response.text}.'
            )
        return response
