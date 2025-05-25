from datetime import datetime

from acutis_api.application.utils.vocacional import (
    verifica_etapa_aprovada,
)
from acutis_api.communication.enums.vocacional import PassosVocacionalEnum
from acutis_api.communication.requests.vocacional import (
    RegistrarFichaVocacionalFormData,
)
from acutis_api.domain.repositories.vocacional import (
    InterfaceVocacionalRepository,
)
from acutis_api.domain.services.file_service import FileServiceInterface
from acutis_api.exception.errors_handler import (
    HttpConflictError,
    HttpNotFoundError,
)


class RegistrarFichaVocacionalUseCase:
    def __init__(
        self,
        s3_service: FileServiceInterface,
        ficha_vocacional_repository: InterfaceVocacionalRepository,
    ):
        self.__ficha_vocacional_repository = ficha_vocacional_repository
        self.__s3_service = s3_service

    def execute(self, request: RegistrarFichaVocacionalFormData):
        ficha_vocacional = request.ficha_vocacional
        foto_vocacional = request.foto_vocacional

        filename = f'foto_vocacional_{
            ficha_vocacional.fk_usuario_vocacional_id
        }_{datetime.now().strftime("%Y%m%d%H%M%S")}'
        file_foto_vocacional = foto_vocacional

        self.__s3_service.salvar_arquivo(file_foto_vocacional, filename)
        if (
            self.__ficha_vocacional_repository.verifica_usuario_vocacional(
                ficha_vocacional.fk_usuario_vocacional_id
            )
            is None
        ):
            raise HttpNotFoundError(
                'Usuário vocacional não encontrado, \
                        é necessário preencher o pré cadastro para seguir.'
            )
        if self.__ficha_vocacional_repository.verifica_ficha_vocacional(
            ficha_vocacional.fk_usuario_vocacional_id
        ):
            raise HttpConflictError('Fichal vocacional já preenchida.')
        etapa = PassosVocacionalEnum.cadastro.value

        busca_pre_cadastro = self.__ficha_vocacional_repository.busca_etapa_vocacional_por_usuario_e_etapa(  # noqa: E501
            ficha_vocacional.fk_usuario_vocacional_id, etapa
        )
        verifica_etapa_aprovada(busca_pre_cadastro, etapa)
        self.__ficha_vocacional_repository.registrar_ficha_vocacional(
            ficha_vocacional, filename
        )
        self.__ficha_vocacional_repository.salvar_alteracoes()
