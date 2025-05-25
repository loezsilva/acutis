from datetime import datetime, timedelta
from typing import Any, Dict, Tuple
from flask import request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Query
from sqlalchemy import func, and_, case, desc, true


from models.actions_leads import ActionsLeads
from models.foto_leads import FotoLeads
from models.leads_sorteados import LeadsSorteados
from models.schemas.admin.get.get_all.get_all_leads import (
    GetAllLeadsResponse,
    GetAllLeadsSchema,
)
from models.users_imports import UsersImports
from models.usuario import Usuario
from services.file_service import FileService


class GetAllLeads:
    def __init__(self, database: SQLAlchemy, file_service: FileService) -> None:
        self.__database = database
        self.__file_service = file_service

    def execute(self):
        self.__page = request.args.get("page", 1, type=int)
        self.__per_page = request.args.get("per_page", 10, type=int)

        final_date_coalense = self.__generate_final_date_coalense()
        filters = self.__get_all_filters(final_date_coalense)
        leads_sorteds_set, actions_sorteds_set = self.__get_leads_and_actions_sorteds()
        leads_query = self.__get_all_leads_query(
            filters, leads_sorteds_set, final_date_coalense
        )
        leads, total = self.__paginate_query(leads_query)
        response = self.__prepare_response(
            leads, total, leads_sorteds_set, actions_sorteds_set
        )

        return response, 200

    def __generate_final_date_coalense(self) -> Any:
        final_date_coalense = func.coalesce(
            UsersImports.updated_at, UsersImports.data_criacao
        ).label("data_final")
        return final_date_coalense

    def __get_all_filters(self, final_date_coalense: Any) -> list:
        filter_mapping = {
            "filtro_nome": lambda value: UsersImports.nome.like(f"%{value}%"),
            "filtro_email": lambda value: UsersImports.email.like(f"%{value}%"),
            "filtro_origem": lambda value: ActionsLeads.nome.like(f"%{value}%"),
            "filtro_data_inicial": lambda value: final_date_coalense
            >= datetime.strptime(value, "%Y-%m-%d"),
            "filtro_data_final": lambda value: final_date_coalense
            <= (
                datetime.strptime(value, "%Y-%m-%d")
                + timedelta(days=1)
                - timedelta(seconds=1)
            ),
            "filtro_nao_baixadas": lambda value : and_(
                FotoLeads.user_download.is_(None),
                FotoLeads.data_download.is_(None),
                FotoLeads.foto.isnot(None) if value == "true" else True
            ),
        }

        filters = []
        for key, filter_func in filter_mapping.items():
            value = request.args.get(key)
            if value:
                filters.append(filter_func(value))

        return filters

    def __get_leads_and_actions_sorteds(self) -> Tuple[set, set]:
        sorteds = self.__database.session.query(
            LeadsSorteados.email, LeadsSorteados.acao_sorteada
        ).all()
        leads_sorteds_set = {email for email, _ in sorteds}
        actions_sorteds_set = {acao for _, acao in sorteds}

        return leads_sorteds_set, actions_sorteds_set

    def __get_all_leads_query(
        self, filters: list, leads_sorteds_set: set, final_date_coalense: Any
    ) -> Query:
        leads_query = (
            self.__database.session.query(
                UsersImports.id,
                UsersImports.nome,
                UsersImports.email,
                UsersImports.phone.label("telefone"),
                UsersImports.intencao,
                ActionsLeads.id.label("fk_acao_id"),
                ActionsLeads.nome.label("origem"),
                FotoLeads.foto,
                FotoLeads.user_download.label("download_usuario_id"),
                func.format(FotoLeads.data_download, "dd/MM/yyyy HH:mm:ss").label(
                    "data_download"
                ),
                func.format(
                    func.coalesce(UsersImports.updated_at, UsersImports.data_criacao),
                    "dd/MM/yyyy HH:mm:ss",
                ).label("data_final"),
                Usuario.nome.label("download_usuario_nome"),
            )
            .join(ActionsLeads, ActionsLeads.id == UsersImports.origem_cadastro)
            .outerjoin(FotoLeads, UsersImports.id == FotoLeads.fk_user_import_id)
            .outerjoin(Usuario, Usuario.id == FotoLeads.user_download)
            .filter(*filters)
        )

        order_conditions = []

        if leads_sorteds_set:
            order_conditions.append(
                case((UsersImports.email.in_(leads_sorteds_set), 0), else_=1)
            )

        order_conditions.append(desc(final_date_coalense))
        leads_query = leads_query.order_by(*order_conditions)

        return leads_query

    def __paginate_query(self, query: Query) -> tuple[UsersImports, int]:
        query_pagination = query.paginate(
            page=self.__page, per_page=self.__per_page, error_out=False
        )
        items, total = query_pagination.items, query_pagination.total
        return items, total

    def __prepare_response(
        self,
        leads: list[UsersImports],
        total: int,
        leads_sorteds_set: set,
        actions_sorteds_set: set,
    ) -> Dict:
        leads_response = []

        for lead in leads:
            foto_lead = (
                self.__file_service.get_public_url(object_name=lead.foto)
                if lead.foto
                else None
            )

            sorteado = None

            if (
                lead.email in leads_sorteds_set
                and lead.fk_acao_id in actions_sorteds_set
            ):
                sorteado = True

            if (
                lead.email not in leads_sorteds_set
                and lead.fk_acao_id in actions_sorteds_set
            ):
                sorteado = False

            lead_data = GetAllLeadsSchema(
                id=lead.id,
                nome=lead.nome,
                email=lead.email,
                telefone=lead.telefone,
                origem=lead.origem,
                criacao=lead.data_final,
                download=(
                    f"{lead.download_usuario_nome} | {lead.data_download}"
                    if lead.data_download
                    else None
                ),
                sorteado=sorteado,
                download_usuario_id=lead.download_usuario_id,
                foto=foto_lead,
                intencao=lead.intencao,
            ).dict()

            leads_response.append(lead_data)

        response = GetAllLeadsResponse(
            page=self.__page,
            total=total,
            leads=leads_response,
        ).dict()

        return response
