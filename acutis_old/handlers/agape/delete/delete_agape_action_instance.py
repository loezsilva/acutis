from http import HTTPStatus
from flask_sqlalchemy import SQLAlchemy

from exceptions.error_types.http_not_found import NotFoundError
from exceptions.error_types.http_unprocessable_entity import (
    HttpUnprocessableEntity,
)
from models.agape.estoque_agape import EstoqueAgape
from models.agape.historico_movimentacao_agape import (
    HistoricoMovimentacaoAgape,
    TipoMovimentacaoEnum,
)
from models.agape.instancia_acao_agape import (
    InstanciaAcaoAgape,
    StatusAcaoAgapeEnum,
)
from models.agape.item_instancia_agape import ItemInstanciaAgape


class DeleteAgapeActionInstance:
    def __init__(self, database: SQLAlchemy) -> None:
        self.__database = database

    def execute(self, fk_instancia_acao_agape_id: int):
        try:
            instancia_acao_agape = self.__get_agape_action_instance_data(
                fk_instancia_acao_agape_id
            )
            self.__return_items_to_stock(instancia_acao_agape)
            self.__delete_instance(instancia_acao_agape)
        except Exception as exception:
            self.__database.session.rollback()
            raise exception

        return {}, HTTPStatus.NO_CONTENT

    def __get_agape_action_instance_data(
        self, fk_instancia_acao_agape_id: int
    ) -> InstanciaAcaoAgape:
        instancia_acao_agape: InstanciaAcaoAgape = self.__database.session.get(
            InstanciaAcaoAgape, fk_instancia_acao_agape_id
        )

        if instancia_acao_agape is None:
            raise NotFoundError("Ciclo da ação não encontrado.")

        if instancia_acao_agape.status != StatusAcaoAgapeEnum.nao_iniciado:
            raise HttpUnprocessableEntity(
                "Somentes ciclos não iniciados podem ser deletados."
            )

        return instancia_acao_agape

    def __return_items_to_stock(
        self, instancia_acao_agape: InstanciaAcaoAgape
    ) -> None:
        itens = ItemInstanciaAgape.query.filter_by(
            fk_instancia_acao_agape_id=instancia_acao_agape.id
        ).all()

        for item in itens:
            estoque = self.__database.session.get(
                EstoqueAgape, item.fk_estoque_agape_id
            )
            estoque.quantidade += item.quantidade
            historico_movimentacao_agape = HistoricoMovimentacaoAgape(
                fk_estoque_agape_id=estoque.id,
                quantidade=item.quantidade,
                tipo_movimentacao=TipoMovimentacaoEnum.entrada,
            )
            self.__database.session.add(historico_movimentacao_agape)
            self.__database.session.delete(item)

    def __delete_instance(
        self, instancia_acao_agape: InstanciaAcaoAgape
    ) -> None:
        self.__database.session.delete(instancia_acao_agape)
        self.__database.session.commit()
