from datetime import datetime, timedelta
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from models.usuario import Usuario
from utils.functions import get_current_time

class UsersByHours:
    def __init__(self, conn: SQLAlchemy):
        self.__conn = conn

    def execute(self) -> tuple:
        try:
            date_now = get_current_time()
            init_interval = date_now - timedelta(days=365)
            cadastros_por_hora = self.__get_registrations_by_hour(init_interval)
            response = self.__format_response(cadastros_por_hora)

            return response

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def __get_registrations_by_hour(self, init_interval: datetime) -> list:
        return (
            self.__conn.session.query(
                self.__conn.func.count(Usuario.id), 
                self.__conn.func.extract('hour', Usuario.data_criacao).label('hour')
            )
            .filter(Usuario.data_criacao >= init_interval, Usuario.deleted_at == None)
            .group_by(self.__conn.func.extract('hour', Usuario.data_criacao))
            .order_by(self.__conn.func.extract('hour', Usuario.data_criacao))
            .all()
        )

    def __format_response(self, cadastros_por_hora: list) -> tuple:
        cadastros_por_hora_dict = {
            f"{hour:02d}:00": count for count, hour in cadastros_por_hora
        }

        return jsonify({"users_per_hour": cadastros_por_hora_dict}), 200
