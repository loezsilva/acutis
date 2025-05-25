from flask import request
from flask_sqlalchemy import SQLAlchemy
from controllers import usuario
from exceptions.error_types.http_not_found import NotFoundError
from models.clifor import Clifor
from models.pedido import Pedido
from models.processamento_pedido import ProcessamentoPedido
from models.usuario import Usuario


class UserTotalDonation:
    def __init__(self, conn: SQLAlchemy, user_id: int):
        self.__conn = conn
        self.__user_id = user_id

    def execute(self):
        self.__verify_user()   
        donation_data = self.__query_user_donations()   
        return self.__format_response(donation_data)   

    def __verify_user(self) -> Usuario:
        user = self.__conn.session.query(Usuario).filter(Usuario.id == self.__user_id).first()
        if user is None:
            raise NotFoundError("Usuário não encontrado!")
        return user

    def __query_user_donations(self) -> tuple:
        result = (
            self.__conn.session.query(
                self.__conn.func.sum(ProcessamentoPedido.valor).label("valor_total"),  
                self.__conn.func.count(ProcessamentoPedido.id).label("quantidade"),               
            )
            .join(Pedido, Pedido.id == ProcessamentoPedido.fk_pedido_id)
            .join(Clifor, Clifor.id == ProcessamentoPedido.fk_clifor_id)
            .join(Usuario, Usuario.id == Clifor.fk_usuario_id)
            .filter(
                Usuario.id == self.__user_id, 
                ProcessamentoPedido.status_processamento == 1,
                ProcessamentoPedido.contabilizar_doacao == 1,
                Pedido.contabilizar_doacao == 1
                )  
        ).first()  

        return result

    def __format_response(self, query_result) -> tuple:

        if query_result:
            valor_total, quantidade = query_result
            donation_data = {
                "valor_doado": round(valor_total or 0.0, 2), 
                "quant_doacoes": quantidade or 0,            
            }
        else:
            donation_data = {
                "valor_doado": 0.0,
                "quant_doacoes": 0,
            }
            
        return donation_data, 200  
