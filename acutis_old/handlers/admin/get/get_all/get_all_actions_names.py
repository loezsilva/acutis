from typing import Dict, List
from flask_sqlalchemy import SQLAlchemy

from models.actions_leads import ActionsLeads
from models.schemas.admin.get.get_all.get_all_actions_names import (
    GetAllActionsNamesResponse,
    GetAllActionsNamesSchema,
)


class GetAllActionsNames:
    def __init__(self, database: SQLAlchemy) -> None:
        self.__database = database

    def execute(self):
        actions_name = self.__get_all_actions_name()
        response = self.__prepare_response(actions_name)

        return response, 200

    def __get_all_actions_name(self) -> List[ActionsLeads]:
        actions_name = self.__database.session.query(
            ActionsLeads.id, ActionsLeads.nome
        ).all()

        return actions_name

    def __prepare_response(self, actions_name: List[ActionsLeads]) -> Dict:
        response = GetAllActionsNamesResponse(
            acoes=[
                GetAllActionsNamesSchema.from_orm(action).dict()
                for action in actions_name
            ],
        ).dict()

        return response
