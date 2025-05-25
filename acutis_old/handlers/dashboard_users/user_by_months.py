from datetime import datetime, timedelta
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from models.usuario import Usuario
from utils.functions import get_current_time

class UsersByMonths:
    def __init__(self, conn: SQLAlchemy):
        self.__conn = conn
        
    def execute(self):
        try:
            date_now = get_current_time()
            init_interval = date_now - timedelta(days=365)  

            cadastros_existente = self.__get_registrations_by_month(init_interval, date_now)

            response = self.__format_response(cadastros_existente)

            return response

        except Exception as e:
            return jsonify({"error": str(e)}), 500


    def __get_registrations_by_month(self, init_interval: str, date_now: str) -> tuple:
        return (
            self.__conn.session.query(
                self.__conn.func.count().label('cadastros'),
                self.__conn.func.month(Usuario.data_criacao).label('month'),
                self.__conn.func.year(Usuario.data_criacao).label('year')
            )
            .filter(
                Usuario.data_criacao >= init_interval,
                Usuario.data_criacao < date_now,
                Usuario.deleted_at == None
                )
            .group_by(self.__conn.func.year(Usuario.data_criacao), self.__conn.func.month(Usuario.data_criacao))
            .order_by(self.__conn.func.year(Usuario.data_criacao), self.__conn.func.month(Usuario.data_criacao))
            .all()
        )

    def __format_response(self, cadastros_existente: tuple) -> tuple:
        cadastros_por_ano_mes = {
            f"{cadastro[1]:02d}/{cadastro[2]}": cadastro[0]   
            for cadastro in cadastros_existente
        }

        cadastros_por_mes_completo_ordenado = [
            {mes: cadastros_por_ano_mes.get(mes, 0)} for mes in cadastros_por_ano_mes.keys()
        ]

        return {"cadastros_by_months": cadastros_por_mes_completo_ordenado}, 200