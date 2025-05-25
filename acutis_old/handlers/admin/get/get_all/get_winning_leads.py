from typing import Dict
from flask import request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, and_
from sqlalchemy.orm import Query

from models.leads_sorteados import LeadsSorteados
from models.schemas.admin.get.get_all.get_winning_leads import (
    GetWinningLeadsFilters,
    GetWinningLeadsResponse,
    GetWinningLeadsSchema,
)
from models.users_imports import UsersImports


class GetWinningLeads:
    def __init__(self, database: SQLAlchemy) -> None:
        self.__database = database

    def execute(self):
        filters = GetWinningLeadsFilters.parse_obj(request.args)
        self.__page = filters.page
        self.__per_page = filters.per_page
        winning_leads_query = self.__get_winning_leads_query(filters)
        winning_leads, total = self.__paginate_query(winning_leads_query)
        response = self.__prepare_response(winning_leads, total)

        return response, 200

    def __get_winning_leads_query(self, filters: GetWinningLeadsFilters) -> Query:
        winning_leads_query = (
            self.__database.session.query(
                LeadsSorteados.id,
                LeadsSorteados.nome,
                LeadsSorteados.email,
                func.format(LeadsSorteados.data_sorteio, "dd/MM/yyyy HH:mm:ss").label(
                    "data_sorteio"
                ),
                LeadsSorteados.acao_sorteada,
                UsersImports.phone.label("tel"),
            )
            .join(
                UsersImports,
                and_(
                    LeadsSorteados.email == UsersImports.email,
                    LeadsSorteados.acao_sorteada == UsersImports.origem_cadastro,
                ),
            )
            .filter(
                (
                    LeadsSorteados.acao_sorteada == filters.filtro_acao_id
                    if filters.filtro_acao_id
                    else True
                )
            )
            .order_by(LeadsSorteados.data_sorteio.desc())
        )

        return winning_leads_query

    def __paginate_query(self, query: Query) -> tuple[LeadsSorteados, int]:
        query_pagination = query.paginate(
            page=self.__page, per_page=self.__per_page, error_out=False
        )
        items, total = query_pagination.items, query_pagination.total
        return items, total

    def __prepare_response(
        self, winning_leads: list[LeadsSorteados], total: int
    ) -> Dict:
        response = GetWinningLeadsResponse(
            page=self.__page,
            total=total,
            leads_sorteados=[
                GetWinningLeadsSchema.from_orm(lead).dict() for lead in winning_leads
            ],
        ).dict()

        return response
