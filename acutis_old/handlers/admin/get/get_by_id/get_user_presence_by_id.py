from typing import List
from flask_sqlalchemy import SQLAlchemy

from exceptions.error_types.http_not_found import NotFoundError
from models.evento_usuario import EventoUsuario
from models.schemas.admin.get.get_by_id.get_user_presence_by_id import (
    GetUserPresenceByIdResponse,
)
from models.usuario import Usuario


class GetUserPresenceById:
    def __init__(self, database: SQLAlchemy):
        self.__database = database

    def execute(self, fk_usuario_id: int):
        user = self.__get_user_data(fk_usuario_id)
        presences = self.__get_presence_data(user.id)
        response = self.__prepare_response(presences)

        return response, 200

    def __get_user_data(self, fk_usuario_id: int) -> Usuario:
        user = self.__database.session.get(Usuario, fk_usuario_id)
        if user is None:
            raise NotFoundError("Usuário não encontrado.")
        return user

    def __get_presence_data(self, fk_usuario_id: int) -> List[EventoUsuario]:
        presence = (
            self.__database.session.query(EventoUsuario)
            .filter_by(fk_usuario_id=fk_usuario_id)
            .all()
        )
        return presence

    def __prepare_response(self, presences: List[EventoUsuario]) -> dict:
        response = GetUserPresenceByIdResponse(
            qtd_campanhas_registradas=len(presences),
            qtd_presencas_registradas=sum(presence.presencas for presence in presences),
        ).dict()
        return response
