from flask import request
from flask_jwt_extended import current_user
from flask_sqlalchemy import SQLAlchemy

from exceptions.error_types.http_not_found import NotFoundError
from exceptions.error_types.http_unauthorized import UnauthorizedError
from models.schemas.users.post.change_password import ChangePasswordRequest
from models.usuario import Usuario
from utils.regex import validate_password


class ChangePassword:
    def __init__(self, database: SQLAlchemy) -> None:
        self.__database = database

    def execute(self):
        user_request = ChangePasswordRequest.parse_obj(request.get_json())
        old_password = user_request.old_password.get_secret_value().strip()
        new_password = validate_password(
            user_request.new_password.get_secret_value().strip()
        )

        user = self.__get_user_data(current_user["id"])
        self.__check_old_password_is_valid(user, old_password)
        self.__update_user_password(user, new_password)
        self.__commit_changes()

        return {"msg": "Senha alterada com sucesso."}, 200

    def __get_user_data(self, user_id: int) -> Usuario:
        user: Usuario = Usuario.query.filter_by(id=user_id, deleted_at=None).first()
        if user is None:
            raise NotFoundError("Usuário não encontrado.")

        return user

    def __check_old_password_is_valid(self, user: Usuario, old_password: str) -> None:
        if user.verify_password(old_password) == False:
            raise UnauthorizedError("A senha atual está incorreta.")

    def __update_user_password(self, user: Usuario, new_password: str) -> None:
        user.password = new_password

    def __commit_changes(self) -> None:
        try:
            self.__database.session.commit()
        except Exception as exception:
            self.__database.session.rollback()
            raise exception
