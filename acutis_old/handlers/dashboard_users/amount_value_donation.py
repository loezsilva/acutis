from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from models.pedido import Pedido
from models.processamento_pedido import ProcessamentoPedido
from utils.functions import get_current_time

class AmountValueDonations:
    def __init__(self, conn: SQLAlchemy):
        self.__conn = conn

    def execute(self) -> tuple:
        try:
            amount_donations = self.__get_total_donations()
            response = self.__format_response(amount_donations)

            return response

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def __get_total_donations(self) -> float:
        today = get_current_time()

        current_month = today.month
        current_year = today.year

        return (
            self.__conn.session.query(self.__conn.func.sum(ProcessamentoPedido.valor))
            .join(Pedido, ProcessamentoPedido.fk_pedido_id == Pedido.id)
            .filter(
                ProcessamentoPedido.status_processamento == 1,
                Pedido.contabilizar_doacao == 1,
                self.__conn.extract("month", ProcessamentoPedido.data_processamento) == current_month,
                self.__conn.extract("year", ProcessamentoPedido.data_processamento) == current_year,
            )
            .scalar()
        ) or 0  

    def __format_response(self, amount_donations: float) -> tuple:
        return jsonify({"amount_donations": round(amount_donations, 2)}), 200
