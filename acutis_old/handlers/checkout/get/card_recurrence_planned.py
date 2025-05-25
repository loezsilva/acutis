from flask_sqlalchemy import SQLAlchemy

from models.clifor import Clifor
from models.pedido import Pedido
from models.processamento_pedido import ProcessamentoPedido
from utils.functions import get_current_time


class CardRecurrencePlanned:
    def __init__(self, conn: SQLAlchemy) -> None:
        self.__conn = conn
        
    def execute(self):
        donations_mades_ids = self.__get_donations_made()
        infos = self.__query_infos(donations_mades_ids)

        return self.__format_response(infos)
        
    def __query_infos(self, donations_mades_ids):
        query_quant = (
            self.__conn.session.query(
                self.__conn.func.count(Pedido.id).label("quant"),
                self.__conn.func.sum(Pedido.valor_total_pedido).label("valor_total")
            )
            .filter(
                Pedido.contabilizar_doacao == 1,
                Pedido.periodicidade == 2,
                Pedido.recorrencia_ativa == 1,
                self.__conn.func.day(Pedido.data_pedido) >= self.__conn.func.day(self.__conn.func.now()),
                Pedido.id.notin_(donations_mades_ids),
            ).first()
        )
        
        return query_quant
    
    def __get_donations_made(self):
        donations_made = (
            self.__conn.session.query(ProcessamentoPedido.fk_pedido_id)
            .filter(
                self.__conn.extract("month", ProcessamentoPedido.data_processamento)
                == get_current_time().month,
                self.__conn.extract("year", ProcessamentoPedido.data_processamento)
                == get_current_time().year,
                ProcessamentoPedido.status_processamento == 1,
                Pedido.contabilizar_doacao == 1,
                Pedido.periodicidade == 2,
            )
            .distinct()
            .subquery()
        )
        
        return donations_made
    
    def __format_response(self, data: tuple):
        quantidade, valor = data
        
        res = {
            "quantidade": quantidade,
            "valor": str(round(valor, 2))
        }
        
        return res, 200