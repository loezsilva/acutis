from http import HTTPStatus
from typing import Dict, List
from models.agape.estoque_agape import EstoqueAgape
from models.schemas.agape.get.get_agape_instance_items import (
    AgapeInstanceItemSchema,
    GetAgapeInstanceItemsResponse,
)
from repositories.interfaces.agape_repository_interface import (
    AgapeRepositoryInterface,
)


class GetAgapeInstanceItems:
    def __init__(self, repository: AgapeRepositoryInterface):
        self.__repository = repository

    def execute(self, fk_instancia_acao_agape_id: int):
        itens = self.__get_agape_instance_items(fk_instancia_acao_agape_id)
        response = self.__prepare_response(itens)
        return response, HTTPStatus.OK

    def __get_agape_instance_items(
        self, fk_instancia_acao_agape_id
    ) -> List[EstoqueAgape]:
        itens = self.__repository.get_agape_instance_items(
            fk_instancia_acao_agape_id
        )
        return itens

    def __prepare_response(self, itens: List[EstoqueAgape]) -> Dict:
        response = GetAgapeInstanceItemsResponse(
            itens_ciclo_agape=[
                AgapeInstanceItemSchema.from_orm(item).dict() for item in itens
            ]
        ).dict()
        return response
