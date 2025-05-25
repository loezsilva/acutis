from flask_sqlalchemy import SQLAlchemy
from models.pedido import Pedido
from models.processamento_pedido import ProcessamentoPedido
from utils.functions import get_current_time

class CardTotalValue:
    def __init__(self, conn: SQLAlchemy) -> None:
        self.__conn = conn

    def execute(self):
        data = self.__get_values_total()
        return self.__format_response(data)

    def __get_values_total(self):
        query_valor_total = (
            self.__conn.session.query(
                self.__conn.func.sum(ProcessamentoPedido.valor).label("valor_total"),
                self.__conn.func.count(Pedido.id).label("quant_pedidos"),
            )
            .join(Pedido, Pedido.id == ProcessamentoPedido.fk_pedido_id)
            .filter(
                ProcessamentoPedido.contabilizar_doacao == 1,
                ProcessamentoPedido.status_processamento == 1,
                Pedido.contabilizar_doacao == 1,
                self.__conn.func.year(ProcessamentoPedido.data_processamento)
                == get_current_time().year,   
            )
            .first()  
        )

        return query_valor_total or (0, 0)

    def __format_response(self, data: tuple) -> dict:
        
        valor_total = data[0] or 0
        quant_pedidos = data[1] or 0

        return {
            "valor_total": round(valor_total, 2),
            "quant_pedidos": quant_pedidos,
        }