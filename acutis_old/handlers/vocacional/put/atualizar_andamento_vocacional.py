from http import HTTPStatus
from typing import Tuple
from flask import request
from exceptions.error_types.http_forbidden import ForbiddenError
from handlers.vocacional.utils.verificar_permissoes_vocacional import verificar_permissoes_vocacional
from repositories.interfaces.vocacional.vocacional_repository_interface import (
    InterfaceVocacionalRepository,
)


class AtualizarAndamentoVocacional:
    def __init__(self, vocacional_repository: InterfaceVocacionalRepository):
        self.__vocacional_repository = vocacional_repository

    def execute(self) -> Tuple[dict, HTTPStatus]:
        http_request = request.get_json()
        usuario_vocacional_id = http_request.get("usuario_vocacional_id")
        acao = http_request.get("acao")
        filtros_permissoes = verificar_permissoes_vocacional()
        usuario_vocacional = self.__vocacional_repository.get_usuario_vocacional(usuario_vocacional_id)

        if (
            usuario_vocacional.genero != filtros_permissoes["editar"]
            and 
            filtros_permissoes["editar"] != "todos"   
        ):
            
            raise ForbiddenError("Você não tem permissão para relizar está ação")

        return self.__vocacional_repository.aprove_or_recuse_vocacional(
            usuario_vocacional_id, acao, http_request
        )
