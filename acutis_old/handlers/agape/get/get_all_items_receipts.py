from http import HTTPStatus
from typing import Dict, List
from exceptions.error_types.http_not_found import NotFoundError
from models.schemas.agape.get.get_all_items_receipts import (
    GetAllItemsReceiptsResponse,
    ItemReceiptSchema,
)
from repositories.interfaces.agape_repository_interface import (
    AgapeRepositoryInterface,
)


class GetAllItemsReceipts:
    def __init__(self, repository: AgapeRepositoryInterface) -> None:
        self.__repository = repository

    def execute(self, fk_instancia_acao_agape_id: int, doacao_agape_id: int):
        self.__check_if_agape_action_instance_exists(
            fk_instancia_acao_agape_id
        )
        itens = self.__repository.get_all_items_receipts(
            fk_instancia_acao_agape_id, doacao_agape_id
        )
        response = self.__prepare_response(itens)

        return response, HTTPStatus.OK

    def __check_if_agape_action_instance_exists(
        self, fk_instancia_acao_agape_id: int
    ):
        instancia_acao_agape = (
            self.__repository.get_agape_action_instance_by_id(
                fk_instancia_acao_agape_id
            )
        )
        if instancia_acao_agape is None:
            raise NotFoundError("Ciclo de ação ágape nao encontrado.")

    def __prepare_response(self, itens: List[ItemReceiptSchema]) -> Dict:
        response = GetAllItemsReceiptsResponse(
            itens_recebidos=[
                ItemReceiptSchema.from_orm(item).dict() for item in itens
            ]
        ).dict()
        return response
