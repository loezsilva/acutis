from flask import request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from sqlalchemy.orm import Query

from models.clifor import Clifor
from models.permissao_usuario import PermissaoUsuario
from models.schemas.admin.get.get_all.get_all_users_permissions import (
    GetAllUsersPermissionsQuery,
    GetAllUsersPermissionsResponse,
    GetAllUsersPermissionsSchema,
)
from models.usuario import Usuario


class GetAllUsersPermissions:
    def __init__(self, database: SQLAlchemy) -> None:
        self.__database = database

    def execute(self):
        filtros = GetAllUsersPermissionsQuery.parse_obj(request.args)
        users_permissions_query = self.__get_all_users_permissions_query(
            filtros
        )
        users_permissions, total = self.__paginate_query(
            users_permissions_query, filtros
        )
        response = self.__prepare_response(users_permissions, total, filtros)

        return response, 200

    def __get_all_users_permissions_query(
        self, filtros: GetAllUsersPermissionsQuery
    ) -> Query:
        users_permissions_query = (
            self.__database.session.query(
                PermissaoUsuario.id,
                PermissaoUsuario.fk_perfil_id,
                Usuario.id.label("fk_usuario_id"),
                Usuario.nome.label("nome_usuario"),
                Usuario.status.label("status_usuario"),
                func.format(Usuario.data_inicio, "dd/MM/yyyy | HH:mm").label(
                    "data_criacao_usuario"
                ),
            )
            .join(Usuario, Usuario.id == PermissaoUsuario.fk_usuario_id)
            .join(Clifor, Clifor.fk_usuario_id == Usuario.id)
            .order_by(PermissaoUsuario.id)
        )

        if filtros.filtro_fk_perfil_id:
            users_permissions_query = users_permissions_query.filter(
                PermissaoUsuario.fk_perfil_id == filtros.filtro_fk_perfil_id
            )

        if filtros.filtro_nome_email_cpf:
            users_permissions_query = users_permissions_query.filter(
                Usuario.nome.contains(filtros.filtro_nome_email_cpf)
                | Usuario.email.contains(filtros.filtro_nome_email_cpf)
                | Clifor.cpf_cnpj.contains(filtros.filtro_nome_email_cpf)
            )

        return users_permissions_query

    def __paginate_query(
        self, query: Query, filtros: GetAllUsersPermissionsQuery
    ) -> tuple[PermissaoUsuario, int]:
        query_pagination = query.paginate(
            page=filtros.page, per_page=filtros.per_page, error_out=False
        )
        items, total = query_pagination.items, query_pagination.total
        return items, total

    def __prepare_response(
        self,
        users_permissions: list[PermissaoUsuario],
        total: int,
        filtros: GetAllUsersPermissionsQuery,
    ) -> dict:
        response = GetAllUsersPermissionsResponse(
            page=filtros.page,
            total=total,
            permissoes_usuarios=[
                GetAllUsersPermissionsSchema.from_orm(user_permission).dict()
                for user_permission in users_permissions
            ],
        ).dict()

        return response
