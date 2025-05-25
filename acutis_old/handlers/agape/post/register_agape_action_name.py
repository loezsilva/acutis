from http import HTTPStatus
from flask_sqlalchemy import SQLAlchemy
from flask import request as flask_request

from exceptions.error_types.http_conflict import ConflictError
from models.agape.acao_agape import AcaoAgape
from models.schemas.agape.post.register_agape_action_name import (
    RegisterAgapeActionNameRequest,
)
from utils.functions import normalize_text


class RegisterAgapeActionName:
    def __init__(self, database: SQLAlchemy):
        self.__database = database

    def execute(self):
        request = RegisterAgapeActionNameRequest.parse_obj(flask_request.json)

        self.__check_if_action_name_already_exists(request.nome)
        self.__register_action_name(request)

        return {
            "msg": "Ação ágape cadastrada com sucesso."
        }, HTTPStatus.CREATED

    def __check_if_action_name_already_exists(self, nome_acao: str) -> None:
        nome_acao_normalizado = normalize_text(nome_acao)

        acoes_agape = AcaoAgape.query.all()
        for acao_cadastrada in acoes_agape:
            acao_cadastrada_normalizada = normalize_text(acao_cadastrada.nome)
            if acao_cadastrada_normalizada == nome_acao_normalizado:
                raise ConflictError(
                    f"Ação {nome_acao} já cadastrada no sistema."
                )

    def __register_action_name(self, action: AcaoAgape) -> None:
        agape_action = AcaoAgape(nome=action.nome)
        self.__database.session.add(agape_action)
        self.__database.session.commit()
