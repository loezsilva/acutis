from http import HTTPStatus
from typing import Dict
from flask_sqlalchemy import SQLAlchemy
from flask import request as flask_request

from exceptions.error_types.http_not_found import NotFoundError
from exceptions.error_types.http_unprocessable_entity import (
    HttpUnprocessableEntity,
)
from models.agape.doacao_agape import DoacaoAgape
from models.agape.familia_agape import FamiliaAgape
from models.agape.instancia_acao_agape import (
    InstanciaAcaoAgape,
    StatusAcaoAgapeEnum,
)
from models.agape.item_doacao_agape import ItemDoacaoAgape
from models.agape.item_instancia_agape import ItemInstanciaAgape
from models.schemas.agape.post.register_agape_donation import (
    RegisterAgapeDonationRequest,
    RegisterAgapeDonationResponse,
)


class RegisterAgapeDonation:
    def __init__(self, database: SQLAlchemy) -> None:
        self.__database = database

    def execute(self):
        request = RegisterAgapeDonationRequest.parse_obj(flask_request.json)
        try:
            self.__validate_family_data(request.fk_familia_agape_id)
            self.__validate_agape_instance_data(
                request.fk_instancia_acao_agape_id
            )
            db_doacao_agape = self.__register_donation(request)
        except Exception as exception:
            self.__database.session.rollback()
            raise exception

        response = self.__prepare_response(db_doacao_agape.id)
        return response, HTTPStatus.CREATED

    def __validate_family_data(self, fk_familia_agape_id: int) -> None:
        familia: FamiliaAgape = self.__database.session.get(
            FamiliaAgape, fk_familia_agape_id
        )
        if familia is None or familia.deleted_at is not None:
            raise NotFoundError("Família não encontrada.")

        if familia.status == False:
            raise HttpUnprocessableEntity(
                "Familia com status inativo para receber doações."
            )

    def __validate_agape_instance_data(
        self, fk_instancia_acao_agape_id: int
    ) -> None:
        instancia_acao_agape: InstanciaAcaoAgape = self.__database.session.get(
            InstanciaAcaoAgape, fk_instancia_acao_agape_id
        )
        if instancia_acao_agape.status != StatusAcaoAgapeEnum.em_andamento:
            raise HttpUnprocessableEntity(
                "Status do ciclo está indisponível para realizar doação."
            )

    def __register_donation(
        self, request: RegisterAgapeDonationRequest
    ) -> DoacaoAgape:
        db_doacao_agape = DoacaoAgape(
            fk_familia_agape_id=request.fk_familia_agape_id
        )
        self.__database.session.add(db_doacao_agape)
        self.__database.session.flush()

        for doacao in request.doacoes:
            item_instancia_agape: ItemInstanciaAgape = (
                self.__database.session.get(
                    ItemInstanciaAgape, doacao.fk_item_instancia_agape_id
                )
            )
            if doacao.quantidade > item_instancia_agape.quantidade:
                raise HttpUnprocessableEntity(
                    "O ciclo da ação possui itens com quantidades insuficientes para realizar esta doação."
                )
            item_doacao_agape = ItemDoacaoAgape(
                fk_item_instancia_agape_id=item_instancia_agape.id,
                fk_doacao_agape_id=db_doacao_agape.id,
                quantidade=doacao.quantidade,
            )
            item_instancia_agape.quantidade -= doacao.quantidade
            self.__database.session.add(item_doacao_agape)

        self.__database.session.commit()
        return db_doacao_agape

    def __prepare_response(self, doacao_agape_id: int) -> Dict:
        response = RegisterAgapeDonationResponse(
            msg="Doação registrada com sucesso.",
            fk_doacao_agape_id=doacao_agape_id,
        ).dict()
        return response
