from http import HTTPStatus

from flask import request

from acutis_api.application.utils.vocacional import envia_email_vocacional
from acutis_api.communication.requests.vocacional import (
    RenviarEmailVocacionalRequest,
)
from acutis_api.domain.repositories.vocacional import (
    InterfaceVocacionalRepository,
)
from acutis_api.exception.errors.not_found import HttpNotFoundError


class ReenviarEmailVocacionalUseCase:
    def __init__(self, vocacional_repository: InterfaceVocacionalRepository):
        self.__vocacional_repository = vocacional_repository

    def execute(self) -> tuple[dict, HTTPStatus]:
        request_data = RenviarEmailVocacionalRequest.model_validate(
            request.get_json()
        )
        vocacional_usuario_id = request_data.usuario_vocacional_id
        vocacional = self.__vocacional_repository.busca_vocacional(
            vocacional_usuario_id
        )

        if not vocacional:
            raise HttpNotFoundError('Vocacional não encontrado.')

        envia_email_vocacional(vocacional)
