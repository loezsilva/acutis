from flask import request, jsonify
from flask_sqlalchemy import SQLAlchemy
from models.usuario import Usuario
from utils.functions import get_current_time
from models.landpage_usuarios import LandpageUsers

class UsersPerHourDaily:
    def __init__(self, conn: SQLAlchemy):
        self.__conn = conn
        self.__http_args = request.args
        self.__filter_campanha = self.__http_args.get("campanha")
        self.__filter_data = self.__http_args.get("data_inicio")

    def execute(self) -> tuple:
        result = self.__get_users_per_hour(self.__filter_campanha, self.__filter_data)
        response = self.__format_response(result)
        return jsonify(response), 200


    def __get_users_per_hour(self, filter_campanha: str, filter_data: str):
        if filter_data:
            date_filter = self.__conn.cast(Usuario.data_inicio, self.__conn.Date) == self.__conn.cast(filter_data, self.__conn.Date)
        else:
            date_filter = self.__conn.cast(Usuario.data_inicio, self.__conn.Date) == self.__conn.cast(get_current_time(), self.__conn.Date)

        if filter_campanha:
            campanhas = list(map(int, filter_campanha.split(",")))
            campanha_filter = LandpageUsers.campaign_id.in_(campanhas)
        else:
            campanha_filter = True  

        return (
            self.__conn.session.query(
                self.__conn.func.count(Usuario.id).label("total_cadastros"),
                self.__conn.func.extract("hour", Usuario.data_inicio).label("hora"),
            )
            .outerjoin(LandpageUsers, LandpageUsers.user_id == Usuario.id)
            .filter(date_filter, campanha_filter, Usuario.deleted_at == None)
            .group_by(self.__conn.func.extract("hour", Usuario.data_inicio))
            .order_by(self.__conn.func.extract("hour", Usuario.data_inicio).asc())
            .all()
        )

    def __format_response(self, result: list) -> list:
        return [
            {"hora": row.hora, "total_cadastros": row.total_cadastros}
            for row in result
        ]
