from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

from models.schemas.admin.get.get_all.get_card_total_leads import (
    GetCardTotalLeadsResponse,
)
from models.users_imports import UsersImports
from models.usuario import Usuario


class GetCardTotalLeads:
    def __init__(self, database: SQLAlchemy) -> None:
        self.__database = database

    def execute(self):
        total_leads = self.__get_total_leads()
        leads_cadastrados = self.__get_leads_cadastrados()
        leads_unicos = self.__get_leads_unicos()
        response = self.__prepare_response(total_leads, leads_cadastrados, leads_unicos)

        return response, 200

    def __get_total_leads(self) -> int:
        total_leads = self.__database.session.query(UsersImports.id).count()
        return total_leads

    def __get_leads_cadastrados(self) -> int:
        leads_cadastrados = (
            self.__database.session.query(func.distinct(UsersImports.email))
            .filter(
                UsersImports.email.in_(self.__database.session.query(Usuario.email))
            )
            .count()
        )
        return leads_cadastrados

    def __get_leads_unicos(self) -> int:
        leads_unicos = self.__database.session.query(
            func.distinct(UsersImports.email)
        ).count()
        return leads_unicos

    def __prepare_response(
        self, total_leads: int, leads_cadastrados: int, leads_unicos: int
    ) -> dict:
        response = GetCardTotalLeadsResponse(
            total_leads=total_leads,
            leads_cadastrados=leads_cadastrados,
            leads_unicos=leads_unicos,
        ).dict()

        return response
