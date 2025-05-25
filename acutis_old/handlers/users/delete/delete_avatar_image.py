from http import HTTPStatus
from flask import Response
from flask_jwt_extended import current_user
from flask_sqlalchemy import SQLAlchemy

from exceptions.error_types.http_not_found import NotFoundError
from models.usuario import Usuario
from services.file_service import FileService


class DeleteAvatarImage:
    def __init__(self, database: SQLAlchemy, file_service: FileService) -> None:
        self.__database = database
        self.__file_service = file_service

    def execute(self):
        user = self.__get_user_data(current_user["id"])

        if user.avatar:
            self.__file_service.delete_object(user.avatar)
            user.avatar = None
            self.__commit_changes()

        return Response(status=HTTPStatus.NO_CONTENT)

    def __get_user_data(self, user_id: int) -> Usuario:
        user = Usuario.query.filter(
            Usuario.id == user_id, Usuario.deleted_at.is_(None)
        ).scalar()
        if user is None:
            raise NotFoundError("Usuário não encontrado.")
        return user

    def __commit_changes(self) -> None:
        try:
            self.__database.session.commit()
        except Exception as exception:
            self.__database.session.rollback()
            raise exception
