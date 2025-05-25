from typing import List

from flask import request as flask_request
from flask_jwt_extended import current_user
from flask_sqlalchemy import SQLAlchemy

from models.processamento_pedido import ProcessamentoPedido
from models.schemas.checkout.post.send_reminder_unpaid_donation import (
    SendReminderUnpaidDonationRequest,
)
from services.file_service import FileService
from templates.email_templates import reminder_unpaid_donation_email_template
from utils.functions import get_current_time
from models.campanha import Campanha
from models.pedido import Pedido
from models.clifor import Clifor
from utils.send_email import send_email
from utils.token_email import generate_token


class SendReminderUnpaidDonation:
    def __init__(self, database: SQLAlchemy, file_service: FileService):
        self.__database = database
        self.__file_service = file_service

    def execute(self):
        request = SendReminderUnpaidDonationRequest.parse_obj(flask_request.json)

        return self.__send_reminder(request.lista_processamento_pedido)

    def __send_reminder(self, lista_processamento_pedido: List[int]):
        for processamento_pedido_id in lista_processamento_pedido:
            result = (
                self.__database.session.query(
                    ProcessamentoPedido,
                    Pedido,
                    Clifor,
                    Campanha,
                )
                .join(Pedido, ProcessamentoPedido.fk_pedido_id == Pedido.id)
                .join(Clifor, Pedido.fk_clifor_id == Clifor.id)
                .join(Campanha, Pedido.fk_campanha_id == Campanha.id)
                .filter(ProcessamentoPedido.id == processamento_pedido_id)
                .first()
            )

            processamento_pedido, pedido, clifor, campanha = result

            if processamento_pedido.status_processamento == 1:
                continue

            foto_campanha = self.__file_service.get_public_url(campanha.filename)

            PAYMENT_TYPE_MAP = {
                2: {
                    "payment_type": "pix",
                    "payment_salt": "send_email_pix_recurrence_payment",
                },
                3: {
                    "payment_type": "invoice",
                    "payment_salt": "send_email_invoice_recurrence_payment",
                },
            }

            payment_type = PAYMENT_TYPE_MAP[pedido.fk_forma_pagamento_id]

            obj_user = {
                "id": clifor.fk_usuario_id,
                "fk_processamento_pedido_id": processamento_pedido.id,
                "fk_pedido_id": pedido.id,
                "fk_gateway_pagamento_id": pedido.fk_gateway_pagamento_id,
            }

            data_vencimento = processamento_pedido.data_criacao.strftime("%d/%m/%Y")

            token = generate_token(obj=obj_user, salt=payment_type.get("payment_salt"))

            html = reminder_unpaid_donation_email_template(
                nome_benfeitor=clifor.nome,
                campanha_id=campanha.id,
                nome_campanha=campanha.titulo,
                foto_campanha=foto_campanha,
                tipo_pagamento=payment_type.get("payment_type"),
                data_vencimento=data_vencimento,
                token=token,
            )

            send_email("Instituto Hesed - Lembrete de Doação", clifor.email, html, 7)

            processamento_pedido.data_lembrete_doacao = get_current_time()
            processamento_pedido.lembrete_enviado_por = current_user["id"]

            self.__database.session.commit()

        return {"msg": "Lembretes enviados com sucesso."}, 200
