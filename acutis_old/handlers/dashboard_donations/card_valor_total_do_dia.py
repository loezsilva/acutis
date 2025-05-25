from flask_sqlalchemy import SQLAlchemy
from models.pedido import Pedido
from models.processamento_pedido import ProcessamentoPedido
from utils.functions import get_current_time


class TotalDailyDonations:
    def __init__(self, conn: SQLAlchemy):
        self.__conn = conn

    def execute(self):
        total_do_dia = self.__get_total_doacoes_dia()   
        return self.__format_response(total_do_dia)   

    def __get_total_doacoes_dia(self) -> float:
        total_do_dia = (
            self.__conn.session.query(self.__conn.func.sum(ProcessamentoPedido.valor))
            .join(Pedido, Pedido.id == ProcessamentoPedido.fk_pedido_id)
            .filter(
                Pedido.contabilizar_doacao == 1,
                ProcessamentoPedido.status_processamento == 1,
                self.__conn.func.month(ProcessamentoPedido.data_processamento)
                == self.__conn.func.month(get_current_time()),
                self.__conn.func.day(ProcessamentoPedido.data_processamento)
                == self.__conn.func.day(get_current_time()),
            )
            .scalar()
        )
        return total_do_dia or 0   

    def __format_response(self, total_do_dia: float) -> tuple:
        return {"total_do_dia": round(total_do_dia, 2)}, 200
