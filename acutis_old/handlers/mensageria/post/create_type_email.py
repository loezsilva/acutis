
from flask import request
from flask_sqlalchemy import SQLAlchemy
from exceptions.error_types.http_conflict import ConflictError
from models.mensageria.tipo_email import TipoEmail
from utils.response import DefaultResponseSchema

class CreateTypeEmail:
    def __init__(self, db: SQLAlchemy) -> None:
        self.__database = db
        self.__tipo_email = request.json.get("tipo_email")

    def execute(self) -> tuple:
        self.__verify_type_email()
        self.__insert_in_database()

        return {"msg": "Tipo de e-mail criado com sucesso!"}, 201

    def __verify_type_email(self):
        email_exists = (
            self.__database.session.query(TipoEmail)
            .filter(TipoEmail.slug == self.__tipo_email)
            .first()
        )
        if email_exists:
            raise ConflictError("Já existe um tipo de email com essa descrição.")

    def __insert_in_database(self):
        try:
            new_type_email = TipoEmail(slug=self.__tipo_email)
            self.__database.session.add(new_type_email)
            self.__database.session.commit()
        except Exception as exception:
            self.__database.session.rollback()
            raise exception