from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from models.usuario import Usuario
from utils.functions import get_current_time

class UsersActualMonth:
    def __init__(self, conn: SQLAlchemy):
        self.__conn = conn

    def execute(self) -> tuple:
        daily_users_data = self.__get_daily_users_for_current_month()
        response = self.__format_response(daily_users_data)
        return response

    def __get_daily_users_for_current_month(self) -> list:

        query = (
            self.__conn.session.query(
                self.__conn.func.count(Usuario.id).label('total_users'),
                self.__conn.func.cast(Usuario.data_criacao, self.__conn.Date).label('creation_date')
            )
            .filter(
                self.__conn.func.month(Usuario.data_criacao) == self.__conn.func.month(get_current_time()),
                self.__conn.func.year(Usuario.data_criacao) == self.__conn.func.year(get_current_time()),
                Usuario.deleted_at == None
            )
            .group_by(self.__conn.func.cast(Usuario.data_criacao, self.__conn.Date))
            .order_by(self.__conn.func.cast(Usuario.data_criacao, self.__conn.Date))
            .all()
        )

        return [{"date": row.creation_date, "total_users": row.total_users} for row in query]

    def __format_response(self, daily_users_data: list) -> tuple:
        formatted_data = {
            data["date"].strftime("%d-%m-%Y"): data["total_users"]
            for data in daily_users_data
        }
        return jsonify({"daily_users": formatted_data}), 200
