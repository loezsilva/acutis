import logging
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from config import EMAIL, ENVIRONMENT, SENDGRID_API_KEY
from models.mensageria.mensageria import Mensageria
from builder import db
from datetime import datetime
import pytz


def send_email(
    assunto: str, destinatario: str, conteudo: any, tipo: int
) -> None:
    if ENVIRONMENT != "production":
        return

    message = Mail(
        from_email=EMAIL,
        to_emails=destinatario,
        subject=assunto,
        html_content=conteudo,
    )

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        res = sg.send(message)

        new_registry_send_email = Mensageria(
            sg_message_id=res.headers.get("X-Message-Id"),
            email=destinatario,
            fk_tipo_email_id=tipo,
            created_at=datetime.now(pytz.timezone("America/Fortaleza")),
        )

        db.session.add(new_registry_send_email)
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        logging.error(f"Erro ao enviar e-mail: {type(e)} - {e}")
        raise Exception("Ocorreu um erro ao enviar o e-mail")
