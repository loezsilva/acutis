from uuid import UUID

from acutis_api.domain.repositories.vocacional import (
    InterfaceVocacionalRepository,
)
from acutis_api.exception.errors.not_found import HttpNotFoundError


class DeletarVocacionalUseCase:
    def __init__(self, vocacional_repository: InterfaceVocacionalRepository):
        self.__vocacional_repository = vocacional_repository

    def execute(self, fk_usuario_vocacional_id: UUID):
        usuario = self.__vocacional_repository.verifica_usuario_vocacional(
            fk_usuario_vocacional_id
        )

        if usuario is None:
            raise HttpNotFoundError('Vocacional não encontrado.')
        self.__vocacional_repository.deletar_vocacional(usuario)
