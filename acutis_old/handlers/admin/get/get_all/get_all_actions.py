from datetime import datetime
from typing import List
from flask import request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from sqlalchemy.orm import Query

from models.actions_leads import ActionsLeads
from models.schemas.admin.get.get_all.get_all_actions import (
    GetAllActionsResponse,
    GetAllActionsSchema,
)
from models.users_imports import UsersImports


class GetAllActions:
    def __init__(self, database: SQLAlchemy) -> None:
        self.__database = database

    def execute(self):
        self.__page = request.args.get("page", 1, type=int)
        self.__per_page = request.args.get("per_page", 10, type=int)

        filters = self.__get_all_filters()
        get_all_actions_query = self.__get_all_actions_query(filters)
        actions, total = self.__paginate_query(get_all_actions_query)
        response = self.__prepare_response(actions, total)

        return response, 200

    def __get_all_filters(self) -> List:
        filter_mapping = {
            "filtro_acao_id": lambda value: ActionsLeads.id == value,
            "filtro_nome": lambda value: ActionsLeads.nome.ilike(f"%{value}%"),
            "filtro_data_inicial": lambda value: self.__database.cast(ActionsLeads.created_at, self.__database.Date) >= self.__database.cast(value, self.__database.Date),
            "filtro_data_final": lambda value: self.__database.cast(ActionsLeads.created_at, self.__database.Date) <= self.__database.cast(value, self.__database.Date)
        }

        filters = []
        for key, filter_func in filter_mapping.items():
            value = request.args.get(key)
            if value:
                filters.append(filter_func(value))

        return filters

    def __get_all_actions_query(self, filters: List) -> Query:
        get_all_actions_query = (
            self.__database.session.query(
                ActionsLeads.id,
                ActionsLeads.nome,
                func.count(UsersImports.id).label("quantidade_leads"),
                func.format(ActionsLeads.created_at, "dd/MM/yyyy").label("criada_em"),
                ActionsLeads.status,
                ActionsLeads.sorteio,
            )
            .outerjoin(UsersImports, ActionsLeads.id == UsersImports.origem_cadastro)
            .filter(*filters)
            .group_by(
                ActionsLeads.id,
                ActionsLeads.nome,
                ActionsLeads.status,
                ActionsLeads.sorteio,
                ActionsLeads.created_at,
            )
            .order_by(ActionsLeads.id)
        )

        return get_all_actions_query

    def __paginate_query(self, query: Query) -> tuple[ActionsLeads, int]:
        query_pagination = query.paginate(
            page=self.__page, per_page=self.__per_page, error_out=False
        )
        items, total = query_pagination.items, query_pagination.total
        return items, total

    def __prepare_response(self, actions: list[ActionsLeads], total: int) -> dict:
        response = GetAllActionsResponse(
            page=self.__page,
            total=total,
            acoes=[GetAllActionsSchema.from_orm(action).dict() for action in actions],
        ).dict()

        return response
