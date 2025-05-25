from http import HTTPStatus
from typing import Tuple
from repositories.interfaces.vocacional.vocacional_repository_interface import (
    InterfaceVocacionalRepository,
)


class RegistrarDesistenciaVocacional:
    def __init__(self, vocacional_repository: InterfaceVocacionalRepository):
        self.__vocacional_repository = vocacional_repository

    def execute(self, usuario_vocacional_id: int) -> Tuple[dict, HTTPStatus]:
        return self.__vocacional_repository.register_desistencia(usuario_vocacional_id)
