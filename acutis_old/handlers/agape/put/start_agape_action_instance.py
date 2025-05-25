from http import HTTPStatus
from flask_sqlalchemy import SQLAlchemy

from exceptions.error_types.http_conflict import ConflictError
from exceptions.error_types.http_not_found import NotFoundError
from exceptions.error_types.http_unprocessable_entity import (
    HttpUnprocessableEntity,
)
from models.agape.instancia_acao_agape import (
    InstanciaAcaoAgape,
    StatusAcaoAgapeEnum,
)
from utils.functions import get_current_time


class StartAgapeActionInstance:
    def __init__(self, database: SQLAlchemy) -> None:
        self.__database = database

    def execute(self, fk_instancia_acao_agape_id: int):
        try:
            instancia_acao_agape = self.__get_agape_action_instance_data(
                fk_instancia_acao_agape_id
            )
            self.__checks_if_exists_instance_in_progress(
                instancia_acao_agape.fk_acao_agape_id
            )
            self.__start_instance(instancia_acao_agape)
            return {
                "msg": "Ciclo da ação iniciado com sucesso."
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

        if instancia_acao_agape.status != StatusAcaoAgapeEnum.nao_iniciado:
            raise HttpUnprocessableEntity(
                "Ciclo da ação já iniciado ou finalizado."
            )

        return instancia_acao_agape

    def __checks_if_exists_instance_in_progress(
        self, fk_acao_agape_id: int
    ) -> None:
        instancia_em_andamento = InstanciaAcaoAgape.query.filter(
            InstanciaAcaoAgape.fk_acao_agape_id == fk_acao_agape_id,
            InstanciaAcaoAgape.status == StatusAcaoAgapeEnum.em_andamento,
        ).first()
        if instancia_em_andamento:
            raise ConflictError(
                "Essa ação ágape já possui um ciclo em andamento."
            )

    def __start_instance(
        self, instancia_acao_agape: InstanciaAcaoAgape
    ) -> None:
        instancia_acao_agape.status = StatusAcaoAgapeEnum.em_andamento
        instancia_acao_agape.data_inicio = get_current_time()
        self.__database.session.commit()
