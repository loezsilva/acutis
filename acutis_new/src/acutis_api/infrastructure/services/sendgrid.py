import logging
import smtplib
from email.mime.text import MIMEText
from http import HTTPStatus

from httpx import Response
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from acutis_api.domain.services.enviar_notificacao import (
    EnviarNotificacaoInterface,
)
from acutis_api.infrastructure.settings import settings
from acutis_api.shared.errors.sendgrid import HttpSendGridError


class SendGridService(EnviarNotificacaoInterface):
    def enviar_email(
        self, destinatario: str, assunto: str, conteudo: str
    ) -> Response | None:
        if settings.ENVIRONMENT != 'producao':
            msg = MIMEText(conteudo, 'html', 'utf-8')
            msg['Subject'] = assunto
            msg['From'] = settings.SENDGRID_EMAIL
            msg['To'] = destinatario

            try:
                with smtplib.SMTP(
                    settings.MAILHOG_HOST, settings.MAILHOG_PORT
                ) as smtp:
                    smtp.send_message(msg)
                logging.info(f'E-mail enviado via MailHog: {destinatario}')
            except Exception as e:
                logging.error(f'Erro ao enviar e-mail via MailHog: {e}')
                raise HttpSendGridError('Erro ao enviar e-mail via MailHog')
            return None

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
            logging.error(f'Ocorreu um erro ao enviar o email.{response.text}')
            raise HttpSendGridError('Ocorreu um erro ao enviar o email.')
        return response
