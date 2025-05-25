from flask_sqlalchemy import SQLAlchemy
from exceptions.error_types.http_not_found import NotFoundError
from models.clifor import Clifor
from models.pedido import Pedido
from models.processamento_pedido import ProcessamentoPedido
from models.usuario import Usuario
from utils.functions import get_current_time

class DonationsUserActualMonth:
    def __init__(self, conn: SQLAlchemy, user_id: int):
        self.__conn = conn
        self.__user_id = user_id
        
    def execute(self):
        user: Usuario = self.__verify_user()
        valor_total, quantidade = self.__query_user_donations()
        return self.__format_response(valor_total, quantidade, user.nome)
    
    def __verify_user(self):
        user = self.__conn.session.query(Usuario).filter(Usuario.id == self.__user_id).first()
        if user is None:
            raise NotFoundError("Usuário inválido")
        return user
    
    def __query_user_donations(self) -> tuple:
        total_donations_current_month = (
            self.__conn.session.query(
                self.__conn.func.sum(ProcessamentoPedido.valor).label("total_valor"),
                self.__conn.func.count(ProcessamentoPedido.id).label("donation_count"),
            )
            .select_from(Pedido)
            .join(ProcessamentoPedido, ProcessamentoPedido.fk_pedido_id == Pedido.id)
            .join(Clifor, Clifor.id == Pedido.fk_clifor_id)
            .join(Usuario, Usuario.id == Clifor.fk_usuario_id)
            .filter(Pedido.contabilizar_doacao == 1)
            .filter(ProcessamentoPedido.status_processamento == 1)
            .filter(Usuario.id == self.__user_id)
            .filter(
                self.__conn.extract("month", ProcessamentoPedido.data_processamento)
                == self.__conn.func.month(get_current_time())
            )
            .filter(
                self.__conn.extract("year", ProcessamentoPedido.data_processamento)
                == self.__conn.func.year(get_current_time())
            )
            .one()
        )
        
        total_valor, quantidade = total_donations_current_month
        
        return (total_valor, quantidade)
        
    def __format_response(self, valor: float, quant: int, user_name: str) -> tuple:
        donation_data = {
            "benfeitor": user_name,
            "user_id": self.__user_id,
            "quantidade_doacoes": quant,
            "valor": str(round(valor, 2)) if valor else "0.00",
        }
        
        return donation_data, 200