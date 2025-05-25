from flask_jwt_extended import current_user
from flask_sqlalchemy import SQLAlchemy
from flask import request as flask_request

from exceptions.error_types.http_bad_request import BadRequestError
from exceptions.error_types.http_not_found import NotFoundError
from models.actions_leads import ActionsLeads
from models.leads_sorteados import LeadsSorteados
from models.schemas.admin.post.confirm_selected_lead import (
    ConfirmSelectedLeadQuery,
    ConfirmSelectedLeadRequest,
)
from utils.functions import get_current_time


class ConfirmSelectedLead:
    def __init__(self, database: SQLAlchemy) -> None:
        self.__database = database

    def execute(self):
        query = ConfirmSelectedLeadQuery.parse_obj(flask_request.args)
        request = ConfirmSelectedLeadRequest.parse_obj(flask_request.json)
        action = self.__get_action_data(request.acao_id)

        if query.sobrepor_sorteio:
            self.__override_winner(request)
        else:
            self.__register_winner(request, action)

        self.__commit_changes()

        return {"msg": "O sorteio foi registrado com sucesso!"}, 200

    def __get_action_data(self, fk_acao_id: int) -> ActionsLeads:
        action: ActionsLeads = self.__database.session.get(ActionsLeads, fk_acao_id)
        if action is None:
            raise NotFoundError("Ação não encontrada.")

        action.sorteio = True

        return action

    def __override_winner(self, request: ConfirmSelectedLeadRequest) -> None:
        lead_sorteado_id = request.lead_sorteado_id
        if lead_sorteado_id is None:
            raise BadRequestError("O ID do lead sorteado é obrigatório.")

        lead_sorteado: LeadsSorteados = self.__database.session.get(
            LeadsSorteados, lead_sorteado_id
        )

        lead_sorteado.nome = request.nome
        lead_sorteado.email = request.email
        lead_sorteado.data_sorteio = get_current_time()
        lead_sorteado.sorteador = current_user["id"]

    def __register_winner(
        self, request: ConfirmSelectedLeadRequest, action: ActionsLeads
    ) -> None:
        lead_sorteado = LeadsSorteados(
            nome=request.nome,
            email=request.email,
            data_sorteio=get_current_time(),
            sorteador=current_user["id"],
            acao_sorteada=action.id,
        )
        self.__database.session.add(lead_sorteado)

    def __commit_changes(self) -> None:
        try:
            self.__database.session.commit()
        except Exception as exception:
            self.__database.session.rollback()
            raise exception
