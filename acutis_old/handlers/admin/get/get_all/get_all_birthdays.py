from flask import request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from sqlalchemy.orm import Query

from models.clifor import Clifor
from models.schemas.admin.get.get_all.get_all_birthdays import (
    GetAllBirthdaysResponse,
    GetAllBirthdaysSchema,
)
from models.usuario import Usuario
from services.file_service import FileService
from utils.functions import calculate_age, get_current_time


class GetAllBirthdays:
    def __init__(self, database: SQLAlchemy, file_service: FileService) -> None:
        self.__database = database
        self.file_service = file_service

    def execute(self):
        self.__page = request.args.get("page", 1, type=int)
        self.__per_page = request.args.get("per_page", 10, type=int)

        aniversariantes_query = self.__get_birtdays_query()
        aniversariantes, total = self.__paginate_query(aniversariantes_query)
        response = self.__prepare_response(aniversariantes, total)

        return response, 200

    def __get_birtdays_query(self) -> Query:
        today = get_current_time()
        actual_month = today.month
        actual_day = today.day

        aniversariantes_query: Query = (
            self.__database.session.query(
                Usuario.id,
                Usuario.avatar.label("foto"),
                Usuario.nome,
                Usuario.email,
                func.format(Clifor.data_nascimento, "dd/MM/yyyy").label(
                    "data_nascimento"
                ),
                Clifor.telefone1.label("telefone"),
            )
            .join(Clifor, Clifor.fk_usuario_id == Usuario.id)
            .filter(
                func.month(Clifor.data_nascimento) == actual_month,
                func.day(Clifor.data_nascimento) == actual_day,
            )
            .order_by(Clifor.data_nascimento)
        )

        return aniversariantes_query

    def __paginate_query(self, query: Query) -> tuple[Usuario, int]:
        query_pagination = query.paginate(
            page=self.__page, per_page=self.__per_page, error_out=False
        )
        items, total = query_pagination.items, query_pagination.total
        return items, total

    def __prepare_response(self, aniversariantes: list[Usuario], total: int) -> dict:
        lista_aniversariantes = [
            GetAllBirthdaysSchema(
                id=aniversariante.id,
                foto=(
                    self.file_service.get_public_url(object_name=aniversariante.foto)
                    if aniversariante.foto
                    else None
                ),
                nome=aniversariante.nome,
                email=aniversariante.email,
                data_nascimento=aniversariante.data_nascimento,
                telefone=aniversariante.telefone,
                idade=calculate_age(aniversariante.data_nascimento),
            ).dict()
            for aniversariante in aniversariantes
        ]

        response = GetAllBirthdaysResponse(
            page=self.__page, total=total, aniversariantes=lista_aniversariantes
        ).dict()

        return response
