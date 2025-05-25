from flask_jwt_extended import current_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, and_

from models.processamento_pedido import ProcessamentoPedido


class GetCardUserDonations:
    def __init__(self, database: SQLAlchemy) -> None:
        self.__database = database

    def execute(self):
        clifor_id = current_user["fk_clifor_id"]

        card_user_donations = self.__get_card_user_donations(clifor_id)
        response = self.__prepare_response(card_user_donations)
        return response, 200

    def __get_card_user_donations(self, clifor_id: int):
        card_user_donations_query = self.__database.session.query(
            func.max(ProcessamentoPedido.data_processamento).label("ultima_doacao"),
            func.count(ProcessamentoPedido.id).label("quant_doacoes"),
            func.coalesce(func.sum(ProcessamentoPedido.valor), 0).label("valor_doado"),
        ).filter(
            and_(
                ProcessamentoPedido.status_processamento == 1,
                ProcessamentoPedido.fk_clifor_id == clifor_id,
            )
        )

        card_user_donations = card_user_donations_query.first()
        return card_user_donations

    def __prepare_response(self, card_user_donations: ProcessamentoPedido) -> dict:
        response = {
            "total_pago_doacoes": {
                "valor_doado": round(card_user_donations.valor_doado, 2),
                "quant_doacoes": card_user_donations.quant_doacoes,
            },
            "ultima_doacao_paga": {
                "ultima_doacao": (
                    card_user_donations.ultima_doacao.strftime("%d/%m/%Y")
                    if card_user_donations.ultima_doacao
                    else None
                )
            },
        }

        return response
