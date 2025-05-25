from typing import Dict, List
from flask import request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Query
from sqlalchemy import and_

from models.campanha import Campanha
from models.clifor import Clifor
from models.evento_usuario import EventoUsuario
from models.foto_campanha import FotoCampanha
from models.schemas.admin.get.get_all.get_all_users_presences import (
    GetAllUsersPresencesResponse,
    GetAllUsersPresencesSchema,
)
from models.usuario import Usuario
from services.file_service import FileService


class GetAllUsersPresences:
    def __init__(self, database: SQLAlchemy, file_service: FileService):
        self.__database = database
        self.__file_service = file_service

    def execute(self):
        self.__page = request.args.get("page", 1, type=int)
        self.__per_page = request.args.get("per_page", 10, type=int)

        filters = self.__get_filters()
        users_presence_query = self.__get_all_users_presence_query(filters)
        users_presence, total = self.__paginate_query(users_presence_query)
        response = self.__prepare_response(users_presence, total)

        return response, 200

    def __get_filters(self) -> List:
        filter_mapping = {
            "filtro_usuario_id": lambda value: EventoUsuario.fk_usuario_id == value,
            "filtro_campanha_id": lambda value: EventoUsuario.fk_campanha_id == value,
            "filtro_numero_documento": lambda value: Clifor.cpf_cnpj.like(f"%{value}%"),
            "filtro_nome_usuario": lambda value: Usuario.nome.like(f"%{value}%"),
            "filtro_nome_campanha": lambda value: Campanha.titulo.like(f"%{value}%"),
            "filtro_email": lambda value: Usuario.email.like(f"%{value}%"),
        }

        filters = []
        for key, filter_func in filter_mapping.items():
            value = request.args.get(key)
            if value:
                filters.append(filter_func(value))

        return filters

    def __get_all_users_presence_query(self, filters: List) -> Query:
        users_presence_query = (
            self.__database.session.query(
                Usuario.id,
                Usuario.nome,
                Usuario.email,
                Clifor.cpf_cnpj.label("numero_documento"),
                EventoUsuario.presencas,
                FotoCampanha.foto,
                Campanha.id.label("fk_campanha_id"),
                Campanha.titulo.label("nome_campanha"),
            )
            .select_from(EventoUsuario)
            .join(Usuario, Usuario.id == EventoUsuario.fk_usuario_id)
            .join(Campanha, Campanha.id == EventoUsuario.fk_campanha_id)
            .join(Clifor, Clifor.fk_usuario_id == Usuario.id)
            .outerjoin(
                FotoCampanha,
                and_(
                    FotoCampanha.fk_usuario_id == Usuario.id,
                    FotoCampanha.fk_campanha_id == EventoUsuario.fk_campanha_id,
                ),
            )
            .filter(*filters)
            .order_by(EventoUsuario.id)
        )

        return users_presence_query

    def __paginate_query(self, query: Query) -> tuple[List[Usuario], int]:
        query_pagination = query.paginate(
            page=self.__page, per_page=self.__per_page, error_out=False
        )
        items, total = query_pagination.items, query_pagination.total
        return items, total

    def __prepare_response(self, users_presence: List[Usuario], total: int) -> Dict:
        presence_response = [
            GetAllUsersPresencesSchema(
                id=presence.id,
                nome=presence.nome,
                email=presence.email,
                numero_documento=presence.numero_documento,
                presencas=presence.presencas,
                foto=(
                    self.__file_service.get_public_url(presence.foto)
                    if presence.foto
                    else None
                ),
                fk_campanha_id=presence.fk_campanha_id,
                nome_campanha=presence.nome_campanha,
            ).dict()
            for presence in users_presence
        ]

        response = GetAllUsersPresencesResponse(
            page=self.__page, total=total, usuarios=presence_response
        ).dict()

        return response
