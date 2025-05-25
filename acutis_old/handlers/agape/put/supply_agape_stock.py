from http import HTTPStatus
from flask import request as flask_request
from flask_sqlalchemy import SQLAlchemy

from exceptions.error_types.http_not_found import NotFoundError
from models.agape.aquisicao_agape import AquisicaoAgape
from models.agape.estoque_agape import EstoqueAgape
from models.agape.historico_movimentacao_agape import (
    HistoricoMovimentacaoAgape,
    TipoMovimentacaoEnum,
)
from models.schemas.agape.put.supply_agape_stock import (
    SupplyAgapeStockRequest,
)


class SupplyAgapeStock:
    def __init__(self, database: SQLAlchemy) -> None:
        self.__database = database

    def execute(self, fk_estoque_agape_id: int):
        try:
            request = SupplyAgapeStockRequest.parse_obj(flask_request.json)
            estoque = self.__validate_stock_exists(fk_estoque_agape_id)
            self.__supply_stock(request, estoque)
        except Exception as exception:
            self.__database.session.rollback()
            raise exception

        return {"msg": "Estoque abastecido com sucesso."}, HTTPStatus.OK

    def __validate_stock_exists(
        self, fk_estoque_agape_id: int
    ) -> EstoqueAgape:
        estoque: EstoqueAgape = self.__database.session.get(
            EstoqueAgape, fk_estoque_agape_id
        )
        if estoque is None:
            raise NotFoundError("Item do estoque não encontrado.")
        return estoque

    def __supply_stock(
        self,
        request: SupplyAgapeStockRequest,
        estoque: EstoqueAgape,
    ):
        aquisicao_estoque = AquisicaoAgape(
            fk_estoque_agape_id=estoque.id,
            quantidade=request.quantidade,
        )
        self.__database.session.add(aquisicao_estoque)

        estoque.quantidade += request.quantidade

        historico_movimentacao = HistoricoMovimentacaoAgape(
            fk_estoque_agape_id=estoque.id,
            quantidade=request.quantidade,
            tipo_movimentacao=TipoMovimentacaoEnum.entrada,
        )
        self.__database.session.add(historico_movimentacao)
        self.__database.session.commit()
