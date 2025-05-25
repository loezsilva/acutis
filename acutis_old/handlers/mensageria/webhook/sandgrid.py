import logging
from builder import db
from exceptions.error_types.http_conflict import ConflictError
from models.mensageria.mensageria import Mensageria
from utils.functions import get_current_time
from flask import request
from exceptions.errors_handler import errors_handler


class SandgridWebhook:
    def __init__(self, logger):
        self.logger = logger

    def execute(self):
        try:
            return self.__update_email_info()
        except Exception as e:
            return errors_handler(e)

    def __update_email_info(self):
        try:
            data = request.json

            if not data or not isinstance(data, list):
                raise ConflictError("Invalid payload")

            for event in data:
                try:
                    email = event.get("email")
                    sg_message_id = event.get("sg_message_id").split(".")[0]
                    event_type = event.get("event")
                    reason = event.get("reason")
                    url = event.get("url")

                    register_send_email: Mensageria = (
                        db.session.query(Mensageria)
                        .filter(
                            Mensageria.email == email,
                            Mensageria.sg_message_id == sg_message_id,
                        )
                        .first()
                    )

                    if register_send_email:
                        register_send_email.status = event_type
                        register_send_email.url = url
                        register_send_email.updated_at = get_current_time()
                        register_send_email.motivo_retorno = reason
                    
                        db.session.commit()
                except Exception as e:
                    return errors_handler(e)

            return {}, 200

        except Exception as e:
            db.session.rollback()
            return errors_handler(e)
