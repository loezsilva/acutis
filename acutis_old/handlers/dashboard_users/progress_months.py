from datetime import datetime, timedelta
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from models.usuario import Usuario
from utils.functions import get_current_time

class UserProgressByMonth:
    def __init__(self, conn: SQLAlchemy):
        self.__conn = conn

    def execute(self) -> tuple:
        try:
            total_users = self.__get_total_users()
            cadastros_por_mes = self.__get_registrations_by_month()
            response = self.__format_response(cadastros_por_mes, total_users)
            return response
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def __get_total_users(self) -> int:
        return (
            self.__conn.session.query(Usuario)
            .filter(Usuario.deleted_at == None)
            .count()
        )

    def __get_registrations_by_month(self) -> list:
        date_now = get_current_time()
        date_12_months_ago = date_now - timedelta(days=365)

        return (
            self.__conn.session.query(
                self.__conn.func.count(Usuario.id),
                self.__conn.func.month(Usuario.data_criacao),
                self.__conn.func.year(Usuario.data_criacao),
            )
            .filter(
                Usuario.deleted_at == None,
                Usuario.data_criacao >= date_12_months_ago
            )
            .group_by(
                self.__conn.func.year(Usuario.data_criacao),
                self.__conn.func.month(Usuario.data_criacao)
            )
            .order_by(
                self.__conn.func.year(Usuario.data_criacao),
                self.__conn.func.month(Usuario.data_criacao)
            )
            .all()
        )

    def __format_response(self, cadastros_por_mes: list, total_users: int) -> tuple:
        data = []
        acumulado = 0
        historico = []
        
        for count, mes, ano in cadastros_por_mes:
            acumulado += count
            historico.append((mes, ano, acumulado))
        
        ajuste = total_users - acumulado
        
        data = [
            {"month": mes, "year": ano, "total_users": total + ajuste}
            for mes, ano, total in historico
        ]
        
        return jsonify({"cadastros_por_mes": data}), 200
