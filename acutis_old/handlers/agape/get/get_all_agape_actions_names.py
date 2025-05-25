from http import HTTPStatus
from typing import Dict, List

from models.agape.acao_agape import AcaoAgape
from models.schemas.agape.get.get_all_agape_actions_names import (
    AgapeActionNameSchema,
    GetAllAgapeActionsNamesResponse,
)


class GetAllAgapeActionsNames:
    def execute(self):
        agape_actions = self.__get_all_agape_actions()
        response = self.__prepare_response(agape_actions)

        return response, HTTPStatus.OK

    def __get_all_agape_actions(self) -> List[AcaoAgape]:
        agape_actions = AcaoAgape.query.all()

        return agape_actions

    def __prepare_response(self, agape_actions: List[AcaoAgape]) -> Dict:
        response = GetAllAgapeActionsNamesResponse(
            acoes_agape=[
                AgapeActionNameSchema.from_orm(action).dict()
                for action in agape_actions
            ]
        ).dict()

        return response
