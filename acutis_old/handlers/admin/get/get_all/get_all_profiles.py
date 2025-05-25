from typing import Dict
from flask import request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from sqlalchemy.orm import Query

from models.perfil import Perfil
from models.permissao_usuario import PermissaoUsuario
from models.schemas.admin.get.get_all.get_all_profiles import (
    GetAllProfilesResponse,
    GetAllProfilesSchema,
)


class GetAllProfiles:
    def __init__(self, database: SQLAlchemy) -> None:
        self.__database = database

    def execute(self):
        self.__page = request.args.get("page", 1, type=int)
        self.__per_page = request.args.get("per_page", 10, type=int)

        profiles_query = self.__get_all_profiles_query()
        profiles, total = self.__paginate_query(profiles_query)
        response = self.__prepare_response(profiles, total)

        return response, 200

    def __get_all_profiles_query(self) -> Query:
        profiles_query = (
            self.__database.session.query(
                Perfil.id,
                Perfil.nome,
                Perfil.status,
                Perfil.super_perfil,
                func.format(Perfil.data_criacao, "dd/MM/yyyy | HH:mm").label(
                    "data_criacao"
                ),
                func.count(PermissaoUsuario.fk_perfil_id).label("quantidade_usuarios"),
            )
            .outerjoin(PermissaoUsuario, PermissaoUsuario.fk_perfil_id == Perfil.id)
            .group_by(
                Perfil.id,
                Perfil.nome,
                Perfil.status,
                Perfil.super_perfil,
                Perfil.data_criacao,
            )
            .order_by(Perfil.id)
        )

        return profiles_query

    def __paginate_query(self, query: Query) -> tuple[Perfil, int]:
        query_pagination = query.paginate(
            page=self.__page, per_page=self.__per_page, error_out=False
        )
        items, total = query_pagination.items, query_pagination.total
        return items, total

    def __prepare_response(self, profiles: list[Perfil], total: int) -> Dict:
        response = GetAllProfilesResponse(
            page=self.__page,
            total=total,
            perfis=[
                GetAllProfilesSchema.from_orm(profile).dict() for profile in profiles
            ],
        ).dict()

        return response
