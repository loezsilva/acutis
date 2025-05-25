from http import HTTPStatus
from flask import request
from exceptions.error_types.http_conflict import ConflictError
from models.schemas.vocacional.post.registrar_pre_cadastro_vocacional_request import (
    RegistrarPreCadastroRequest,
)
from models.vocacional.usuario_vocacional import UsuarioVocacional
from repositories.interfaces.vocacional.vocacional_repository_interface import (
    InterfaceVocacionalRepository,
)
from templates.email_templates import send_email_pre_cadastro_vocacional_recebido
from utils import send_email


class RegistrarPreCadastro:
    def __init__(self, vocacional_repository: InterfaceVocacionalRepository):
        self.__vocacional_repository = vocacional_repository

    def execute(self) -> tuple[dict, HTTPStatus]:
        data_pre_cadastro = RegistrarPreCadastroRequest.parse_obj(request.get_json())
        self.__vocacional_repository.pre_register_vocacional(data_pre_cadastro)
        return {"msg": "Pré-cadastro realizado com sucesso!"}, HTTPStatus.CREATED
