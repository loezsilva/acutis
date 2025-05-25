from typing import List, Optional
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

from exceptions.error_types.http_not_found import NotFoundError
from models.actions_leads import ActionsLeads
from models.leads_sorteados import LeadsSorteados
from models.schemas.admin.get.get_by_id.get_action_details_by_id import (
    GetActionDetailsByIdResponse,
)
from models.users_imports import UsersImports
from models.usuario import Usuario
from services.file_service import FileService


class GetActionDetailsById:
    def __init__(self, database: SQLAlchemy, file_service: FileService) -> None:
        self.__database = database
        self.file_service = file_service

    def execute(self, fk_acao_id: int):
        action = self.__get_action_by_id(fk_acao_id)
        total_leads = self.__get_total_leads(action.id)
        winning_leads = self.__get_winning_leads(action.id)
        response = self.__prepare_response(action, total_leads, winning_leads)

        return response, 200

    def __get_action_by_id(self, fk_acao_id: int) -> ActionsLeads:
        action = (
            self.__database.session.query(
                ActionsLeads.id,
                ActionsLeads.nome,
                ActionsLeads.titulo,
                ActionsLeads.descricao,
                ActionsLeads.background,
                ActionsLeads.banner,
                ActionsLeads.status,
                ActionsLeads.preenchimento_foto,
                ActionsLeads.label_foto,
                ActionsLeads.sorteio,
                func.format(ActionsLeads.created_at, "dd/MM/yyyy HH:mm:ss").label(
                    "criado_em"
                ),
                Usuario.nome.label("cadastrado_por"),
            )
            .outerjoin(Usuario, Usuario.id == ActionsLeads.cadastrado_por)
            .filter(ActionsLeads.id == fk_acao_id)
            .first()
        )

        if action is None:
            raise NotFoundError("Ação não encontrada.")

        return action

    def __get_total_leads(self, fk_acao_id: int) -> int:
        total_leads = (
            self.__database.session.query(UsersImports.id)
            .filter(UsersImports.origem_cadastro == fk_acao_id)
            .count()
        )

        return total_leads

    def __get_winning_leads(self, fk_acao_id: int) -> Optional[List[LeadsSorteados]]:
        leads_sorteados = (
            self.__database.session.query(
                LeadsSorteados.nome,
                func.format(LeadsSorteados.data_sorteio, "dd/MM/yyyy HH:mm:ss").label(
                    "data_sorteio"
                ),
                Usuario.nome.label("sorteador"),
            )
            .join(Usuario, Usuario.id == LeadsSorteados.sorteador)
            .filter(LeadsSorteados.acao_sorteada == fk_acao_id)
            .all()
        )

        return leads_sorteados

    def __prepare_response(
        self,
        action: ActionsLeads,
        total_leads: int,
        winning_leads: Optional[List[LeadsSorteados]],
    ) -> dict:
        response = GetActionDetailsByIdResponse(
            id=action.id,
            nome=action.nome,
            titulo=action.titulo,
            descricao=action.descricao,
            background=(
                self.file_service.get_public_url(object_name=action.background)
                if action.background
                else None
            ),
            banner=(
                self.file_service.get_public_url(object_name=action.banner)
                if action.banner
                else None
            ),
            status=action.status,
            preenchimento_foto=action.preenchimento_foto,
            label_foto=action.label_foto,
            sorteio=action.sorteio,
            total_leads=total_leads,
            criado_em=action.criado_em,
            cadastrado_por=action.cadastrado_por,
            sorteados=[winning.nome for winning in winning_leads],
            sorteador=winning_leads[0].sorteador if winning_leads else None,
            data_sorteio=winning_leads[0].data_sorteio if winning_leads else None,
        ).dict()

        return response
