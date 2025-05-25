from flask_sqlalchemy import SQLAlchemy

from models.schemas.admin.get.get_by_id.get_total_leads_by_action_id import (
    GetTotalLeadsByActionIdResponse,
)
from models.users_imports import UsersImports


class GetTotalLeadsByActionId:
    def __init__(self, database: SQLAlchemy) -> None:
        self.__database = database

    def execute(self, fk_acao_id: int):
        total_leads = self.__get_total_leads(fk_acao_id)
        response = self.__prepare_response(total_leads)
        return response, 200

    def __get_total_leads(self, fk_acao_id: int) -> int:
        total_leads = (
            self.__database.session.query(UsersImports.id)
            .filter(UsersImports.origem_cadastro == fk_acao_id)
            .count()
        )
        return total_leads

    def __prepare_response(self, total_leads: int) -> dict:
        response = GetTotalLeadsByActionIdResponse(total_leads=total_leads).dict()

        return response
