from http import HTTPStatus
from typing import Dict
from models.schemas.agape.get.get_cards_stock_items_statistics import (
    GetCardsStockItemsStatisticsResponse,
)
from repositories.interfaces.agape_repository_interface import (
    AgapeRepositoryInterface,
)
from repositories.schemas.agape_schemas import (
    GetLastAgapeActionSchema,
    GetLastStockSupplySchema,
    GetNumberStockItemsSchema,
)


class GetCardsStockItemsStatistics:
    def __init__(self, repository: AgapeRepositoryInterface) -> None:
        self.__repository = repository

    def execute(self):
        itens = self.__repository.get_number_stock_items()
        ultima_acao = self.__repository.get_last_agape_action()
        ultima_entrada = self.__repository.get_last_stock_supply()
        response = self.__prepare_response(itens, ultima_acao, ultima_entrada)

        return response, HTTPStatus.OK

    def __prepare_response(
        self,
        itens: GetNumberStockItemsSchema,
        ultima_acao: GetLastAgapeActionSchema,
        ultima_entrada: GetLastStockSupplySchema,
    ) -> Dict:
        response = GetCardsStockItemsStatisticsResponse(
            itens_em_estoque=f"{itens.em_estoque} | Em estoque",
            ultima_acao=(
                f"{ultima_acao.data.strftime('%d/%m/%Y')} | {ultima_acao.quantidade_itens_doados} Itens"
                if ultima_acao
                else "Não possui"
            ),
            ultima_entrada=(
                f"{ultima_entrada.data.strftime('%d/%m/%Y')} | {ultima_entrada.quantidade} Itens"
                if ultima_entrada
                else "Não possui"
            ),
        ).dict()

        return response
