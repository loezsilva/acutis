from uuid import UUID

from acutis_api.communication.enums.vocacional import (
    PassosVocacionalStatusEnum,
)
from acutis_api.domain.repositories.vocacional import (
    InterfaceVocacionalRepository,
)
from acutis_api.exception.errors_handler import (
    HttpConflictError,
    HttpNotFoundError,
)


class RegistrarDesistenciaVocacionalUseCase:
    def __init__(self, vocacional_repository: InterfaceVocacionalRepository):
        self.__vocacional_repository = vocacional_repository

    def execute(self, usuario_vocacional_id: UUID) -> dict:
        etapa_atual = self.__vocacional_repository.busca_etapa_atual(
            usuario_vocacional_id
        )

        if etapa_atual is None:
            raise HttpNotFoundError('Etapa vocacional não encontrada.')

        if etapa_atual.status == PassosVocacionalStatusEnum.desistencia:
            raise HttpConflictError('Desistência já realizada anteriormente.')
        self.__vocacional_repository.registrar_desistencia(
            usuario_vocacional_id, etapa_atual
        )
        self.__vocacional_repository.salvar_alteracoes()
