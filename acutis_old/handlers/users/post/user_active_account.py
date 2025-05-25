from typing import Dict, Optional
from flask import Response, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_sqlalchemy import SQLAlchemy

from exceptions.error_types.http_bad_request import BadRequestError
from exceptions.error_types.http_unauthorized import UnauthorizedError
from models.campanha import Campanha
from models.token import Token
from models.usuario import Usuario
from utils.token_email import verify_token


class UserActiveAccount:
    def __init__(self, database: SQLAlchemy) -> None:
        self.__database = database

    def execute(self, token: str) -> Response:
        payload = self.__verify_token(token)
        tipo_cadastro = payload.get("tipo_cadastro", None)

        if tipo_cadastro != "alistamento":
            self.__check_token_has_been_used(token)

        email = payload["email"]
        user = self.__get_user_data(email)
        campanha_origem = self.__validate_origin_campaign(
            payload.get("campanha_origem", None)
        )
        self.__active_account_user(user, token, tipo_cadastro)
        self.__commit_changes()

        if tipo_cadastro == "alistamento":
            response = self.__prepare_response_alistamento(payload)
        else:
            response = self.__prepare_response(user, campanha_origem)

        return response, 200

    def __verify_token(self, token: str) -> dict:
        payload = verify_token(token, salt="active_account_confirmation")
        return payload

    def __check_token_has_been_used(self, token: str) -> None:
        if Token.query.filter_by(token=token.lower()).first():
            raise UnauthorizedError("Token já utilizado.")

    def __get_user_data(self, email: str) -> Usuario:
        user: Usuario = Usuario.query.filter_by(
            email=email, deleted_at=None
        ).first()
        if user is None:
            raise BadRequestError("Usuário não encontrado.")
        return user

    def __validate_origin_campaign(
        self, campanha_origem: Optional[int]
    ) -> Optional[int]:
        if campanha_origem:
            campanha: Optional[Campanha] = self.__database.session.get(
                Campanha, campanha_origem
            )
            if campanha is None or not (campanha.status and campanha.publica):
                campanha_origem = None

        return campanha_origem

    def __active_account_user(
        self, user: Usuario, token: str, tipo_cadastro: Optional[str] = None
    ):
        user.status = True
        if tipo_cadastro != "alistamento":
            register_token = Token(token=token.lower())

            self.__database.session.add(register_token)

    def __commit_changes(self) -> None:
        try:
            self.__database.session.commit()
        except Exception as exception:
            self.__database.session.rollback()
            raise exception

    def __prepare_response_alistamento(self, payload: Dict) -> Response:
        response = {
            "usuario_id": payload.get("usuario_id"),
            "email": payload.get("email"),
            "telefone": payload.get("telefone"),
            "nome": payload.get("nome"),
            "pais": payload.get("pais"),
        }

        return jsonify(response)

    def __prepare_response(
        self,
        user: Usuario,
        campanha_origem: Optional[int],
    ) -> Response:
        response = {
            "access_token": create_access_token(identity=user.id),
            "refresh_token": create_refresh_token(identity=user.id),
            "campanha_origem": campanha_origem,
        }

        return jsonify(response)
