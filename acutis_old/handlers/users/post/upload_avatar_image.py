from flask import request
from flask_jwt_extended import current_user
from flask_sqlalchemy import SQLAlchemy

from exceptions.error_types.http_not_found import NotFoundError
from models.usuario import Usuario
from services.file_service import FileService


class UploadAvatarImage:
    def __init__(self, database: SQLAlchemy, file_service: FileService) -> None:
        self.__database = database
        self.__file_service = file_service

    def execute(self):
        file = request.files["image"]
        user = self.__get_user_data(current_user["id"])

        filename = self.__file_service.upload_image(file=file, filename=user.avatar)
        user.avatar = filename
        self.__commit_changes()

        return {"msg": "Foto de perfil atualizada com sucesso!"}

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
