from http import HTTPStatus
from typing import Tuple, Dict
from flask import request
from models.schemas.vocacional.post.registrar_cadastro_vocacional_request import (
    RegistrarCadastroVocacionalRequest,
)
from repositories.interfaces.vocacional.vocacional_repository_interface import (
    InterfaceVocacionalRepository,
)


class RegistrarCadastroVocacional:
    def __init__(self, vocacional_repository: InterfaceVocacionalRepository):
        self.__vocacional_repository = vocacional_repository

    def execute(self) -> Tuple[Dict, HTTPStatus]:
        http_request = RegistrarCadastroVocacionalRequest.parse_obj(request.get_json())
        return self.__vocacional_repository.register_cadastro_vocacional(http_request)
