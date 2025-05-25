from flask import request
from flask_sqlalchemy import SQLAlchemy
from itsdangerous import BadSignature

from exceptions.error_types.http_bad_request import BadRequestError
from exceptions.error_types.http_unauthorized import UnauthorizedError

from models.schemas.auth.post.new_password import NewPasswordQuery, NewPasswordRequest
from models.token import Token
from models.usuario import Usuario
from utils.regex import validate_password
from utils.token_email import verify_token


class NewPassword:
    def __init__(self, database: SQLAlchemy) -> None:
        self.__database = database

    def execute(self):
        req = NewPasswordRequest.parse_obj(request.get_json())
        query_params = NewPasswordQuery.parse_obj(request.args)
        new_password = validate_password(req.new_password.get_secret_value().strip())
        token = query_params.token
        email = self.__verify_token(token)
        self.__check_token_has_been_used(token)
        user = self.__get_user_data(email)
        self.__update_user_password(user, new_password)
        self.__commit_changes()

        return {"msg": "Senha alterada com sucesso."}, 200

    def __verify_token(self, token: str) -> str:
        try:
            email = verify_token(
                token, salt="reset_password_confirmation", max_age=1 * 60 * 60
            )
            return email
        except BadSignature:
            raise UnauthorizedError("Token inválido!")

    def __check_token_has_been_used(self, token: str) -> None:
        if Token.query.filter_by(token=token.lower()).first():
            raise UnauthorizedError("Token já utilizado.")

    def __get_user_data(self, email: str) -> Usuario:
        user: Usuario = Usuario.query.filter_by(email=email, deleted_at=None).first()
        if user is None:
            raise BadRequestError("Usuário não encontrado.")

        return user

    def __update_user_password(self, user: Usuario, new_password: str) -> None:
        user.password = new_password
        user.status = 1

    def __commit_changes(self) -> None:
        try:
            self.__database.session.commit()
        except Exception as exception:
            self.__database.session.rollback()
            raise exception
