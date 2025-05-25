from datetime import datetime, timedelta
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from models.usuario import Usuario
from utils.functions import get_current_time

class UsersByWeekday:
    def __init__(self, conn: SQLAlchemy):
        self.__conn = conn

    def execute(self) -> tuple:
        try:
            date_now = get_current_time()
            init_interval = date_now - timedelta(days=365)

            users_per_day = self.__get_users_per_weekday(init_interval)

            response = self.__format_response(users_per_day)

            return response

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def __get_users_per_weekday(self, init_interval: datetime) -> list:
        return (
            self.__conn.session.query(
                self.__conn.func.count(Usuario.id),
                self.__conn.func.extract('dow', Usuario.data_criacao).label('weekday')
            )
            .filter(Usuario.data_criacao >= init_interval, Usuario.deleted_at == None)
            .group_by(self.__conn.func.extract('dow', Usuario.data_criacao))
            .order_by(self.__conn.func.extract('dow', Usuario.data_criacao))
            .all()
        )

    def __format_response(self, users_per_day: list) -> tuple:
        day_of_weeks = {
            0: "Domingo",
            1: "Segunda-feira",
            2: "Terça-feira",
            3: "Quarta-feira",
            4: "Quinta-feira",
            5: "Sexta-feira",
            6: "Sábado",
        }

        users_per_weekday = [
            {day_of_weeks[(day % 7)]: count} for count, day in users_per_day
        ]

        return jsonify({"day_of_weeks": users_per_weekday}), 200
