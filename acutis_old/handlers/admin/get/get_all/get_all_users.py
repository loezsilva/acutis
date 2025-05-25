from datetime import datetime
from flask import request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Query
from models.clifor import Clifor
from models.landpage_usuarios import LandpageUsers
from models.schemas.admin.get.get_all.get_all_users import (
    GetAllUsersResponse,
    GetAllUsersSchema,
)
from models.usuario import Usuario

class GetAllUsers:
    def __init__(self, database: SQLAlchemy) -> None:
        self.__database = database

    def execute(self):
        self.__page = request.args.get("page", 1, type=int)
        self.__per_page = request.args.get("per_page", 10, type=int)
        self.__campaign_id = request.args.get("filtro_campanha_origem")
        
        filters = self.__get_query_filters()
        get_all_users_query = self.__get_all_users_query(filters)
        users, total, pages = self.__paginate_query(get_all_users_query)
        response = self.__prepare_response(users, total, pages)
        return response, 200

    def __get_query_filters(self) -> list:
        filter_mapping = {
            "filtro_id_usuario": lambda value: Usuario.id.like(f"%{value}%"),
            "filtro_numero_documento": lambda value: Clifor.cpf_cnpj.like(f"%{value}%"),
            "filtro_status": lambda value: Usuario.status == value,
            "filtro_email": lambda value: Usuario.email.like(f"%{value}%"),
            "filtro_nome": lambda value: Usuario.nome.like(f"%{value}%"),
            "filtro_telefone": lambda value: Clifor.telefone1 == value,
            "filtro_data_cadastro_inicial": lambda value: self.__database.cast(Usuario.data_inicio, self.__database.Date)
            >= self.__database.cast(value, self.__database.Date),
            "filtro_data_cadastro_final": lambda value: self.__database.cast(Usuario.data_inicio, self.__database.Date)
            <= self.__database.cast(value, self.__database.Date),
            "filtro_data_ultimo_acesso_inicial": lambda value: self.__database.cast(Usuario.data_ultimo_acesso, self.__database.Date)
            >= self.__database.cast(value, self.__database.Date),
            "filtro_data_ultimo_acesso_final": lambda value: self.__database.cast(Usuario.data_ultimo_acesso, self.__database.Date)
            <= self.__database.cast(value, self.__database.Date),
        }
        filters = []
        for key, filter_func in filter_mapping.items():
            value = request.args.get(key)
            if value and key != "filtro_campanha_origem":   
                filters.append(filter_func(value))
        return filters

    def __get_all_users_query(self, filters: list) -> Query:
        get_all_users_query = (
            self.__database.session.query(Usuario)
            .join(Clifor, Usuario.id == Clifor.fk_usuario_id)
        )

        if self.__campaign_id:
            get_all_users_query = get_all_users_query.outerjoin(
                LandpageUsers,
                (Usuario.id == LandpageUsers.user_id) & 
                (LandpageUsers.campaign_id == self.__campaign_id)
            ).filter(Usuario.campanha_origem == self.__campaign_id)

        get_all_users_query = (
            get_all_users_query
            .filter(Usuario.deleted_at.is_(None), *filters)
            .order_by(Usuario.id)
        )
        
        return get_all_users_query

    def __paginate_query(self, query: Query) -> tuple[Usuario, int]:
        query_pagination = query.paginate(
            page=self.__page, per_page=self.__per_page, error_out=False
        )
        items, total, pages = query_pagination.items, query_pagination.total, query_pagination.pages
        return items, total, pages

    def __prepare_response(self, users: list[Usuario], total: int, pages: int) -> dict:
        response = GetAllUsersResponse(
            page=self.__page,
            pages=pages,
            total=total,
            usuarios=[GetAllUsersSchema.from_orm(user).dict() for user in users],
        ).dict()
        return response