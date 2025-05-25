from http import HTTPStatus
from typing import List
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
from utils.functions import get_current_time


class FinishAgapeActionInstance:
    def __init__(self, database: SQLAlchemy) -> None:
        self.__database = database

    def execute(self, fk_instancia_acao_agape_id: int):
        try:
            instancia_acao_agape = self.__get_agape_action_instance_data(
                fk_instancia_acao_agape_id
            )
            self.__return_remaining_items(instancia_acao_agape)
            self.__finish_instance(instancia_acao_agape)

            return {
                "msg": "Ciclo da ação finalizado com sucesso."
            }, HTTPStatus.OK
        except Exception as exception:
            self.__database.session.rollback()
            raise exception

    def __get_agape_action_instance_data(
        self, fk_instancia_acao_agape_id: int
    ) -> InstanciaAcaoAgape:
        instancia_acao_agape: InstanciaAcaoAgape = self.__database.session.get(
            InstanciaAcaoAgape, fk_instancia_acao_agape_id
        )

        if instancia_acao_agape is None:
            raise NotFoundError("Ciclo da ação não encontrado.")

        if instancia_acao_agape.status != StatusAcaoAgapeEnum.em_andamento:
            raise HttpUnprocessableEntity(
                "Ciclo da ação ainda não foi iniciado ou já foi finalizado."
            )

        return instancia_acao_agape

    def __return_remaining_items(
        self, instancia_acao_agape: InstanciaAcaoAgape
    ) -> None:
        itens_instancia_agape: List[ItemInstanciaAgape] = (
            ItemInstanciaAgape.query.filter_by(
                fk_instancia_acao_agape_id=instancia_acao_agape.id
            ).all()
        )

        for item in itens_instancia_agape:
            if item.quantidade > 0:
                estoque_agape = EstoqueAgape.query.filter_by(
                    id=item.fk_estoque_agape_id
                ).first()
                estoque_agape.quantidade += item.quantidade
                historico_movimentacao = HistoricoMovimentacaoAgape(
                    fk_estoque_agape_id=estoque_agape.id,
                    quantidade=item.quantidade,
                    tipo_movimentacao=TipoMovimentacaoEnum.entrada,
                )
                self.__database.session.add(historico_movimentacao)
                item.quantidade = 0

    def __finish_instance(
        self, instancia_acao_agape: InstanciaAcaoAgape
    ) -> None:
        instancia_acao_agape.status = StatusAcaoAgapeEnum.finalizado
        instancia_acao_agape.data_termino = get_current_time()
        self.__database.session.commit()
