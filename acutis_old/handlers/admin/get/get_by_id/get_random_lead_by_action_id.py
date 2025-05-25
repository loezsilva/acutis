from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

from exceptions.error_types.http_not_found import NotFoundError
from models.actions_leads import ActionsLeads
from models.clifor import Clifor
from models.schemas.admin.get.get_by_id.get_random_lead_by_action_id import (
    GetRandomLeadByActionIdResponse,
)
from models.users_imports import UsersImports
from models.usuario import Usuario


class GetRandomLeadByActionId:
    def __init__(self, database: SQLAlchemy) -> None:
        self.__database = database

    def execute(self, fk_acao_id: int):
        self.__check_if_action_exists(fk_acao_id)
        lead = self.__get_random_lead(fk_acao_id)
        response = self.__prepare_response(lead)

        return response, 200

    def __check_if_action_exists(self, fk_acao_id: int) -> None:
        if self.__database.session.get(ActionsLeads, fk_acao_id) is None:
            raise NotFoundError("Ação não encontrada.")

    def __get_random_lead(self, fk_acao_id: int) -> UsersImports:
        data_criacao = func.coalesce(
            UsersImports.updated_at,
            UsersImports.data_criacao,
        ).label("data_criacao")

        query_imports = self.__database.session.query(
            UsersImports.nome,
            UsersImports.email,
            UsersImports.phone.label("telefone"),
            func.format(data_criacao, "dd/MM/yyyy - HH:mm:ss").label("cadastrado_em"),
        ).filter_by(origem_cadastro=fk_acao_id)

        query_usuarios = (
            self.__database.session.query(
                Usuario.nome,
                Usuario.email,
                Clifor.telefone1.label("telefone"),
                func.format(Usuario.data_criacao, "dd/MM/yyyy - HH:mm:ss").label(
                    "cadastrado_em"
                ),
            )
            .select_from(Usuario)
            .join(Clifor, Clifor.fk_usuario_id == Usuario.id)
            .filter(Usuario.origem_cadastro == fk_acao_id)
        )

        combined_query = query_imports.union_all(query_usuarios).order_by(func.newid())

        lead = combined_query.first()

        if lead is None:
            raise NotFoundError("Nenhum lead encontrado.")

        return lead

    def __prepare_response(self, lead: UsersImports) -> dict:
        response = GetRandomLeadByActionIdResponse.from_orm(lead).dict()

        return response
