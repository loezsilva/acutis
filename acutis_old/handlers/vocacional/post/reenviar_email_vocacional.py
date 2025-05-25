from http import HTTPStatus
from flask import request
from exceptions.error_types.http_forbidden import ForbiddenError
from handlers.vocacional.utils.reenvia_email_vocacional import envia_email_vocacional
from handlers.vocacional.utils.verificar_permissoes_vocacional import verificar_permissoes_vocacional
from models.schemas.vocacional.post.reenviar_email_vocacioanal_request import (
    RenviarEmailVocacionalRequest,
)
from repositories.interfaces.vocacional.vocacional_repository_interface import (
    InterfaceVocacionalRepository,
)


class ReenviarEmailVocacional:
    def __init__(self, vocacional_repository: InterfaceVocacionalRepository):
        self.__vocacional_repository = vocacional_repository

    def execute(self) -> tuple[dict, HTTPStatus]:
        request_data = RenviarEmailVocacionalRequest.parse_obj(request.get_json())
        vocacional_usuario_id = request_data.usuario_vocacional_id
        vocacional = self.__vocacional_repository.get_usuario_vocacional(
            vocacional_usuario_id
        )

        filtros_permissoes = verificar_permissoes_vocacional()

        if (
            vocacional.genero != filtros_permissoes["acessar"]
            and 
            filtros_permissoes["acessar"] != "todos"   
        ):
            
            raise ForbiddenError("Você não tem permissão para relizar está ação")

        envia_email_vocacional(vocacional)
        return {"msg": "Email reenviado com sucesso."}, HTTPStatus.OK
