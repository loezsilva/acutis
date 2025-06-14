import uuid

from acutis_api.communication.requests.agape import (
    RegistrarRecibosRequestFormData,
)
from acutis_api.domain.repositories.agape import AgapeRepositoryInterface
from acutis_api.domain.repositories.schemas.agape import (
    FotoFamiliaAgapeSchema,
)
from acutis_api.domain.services.file_service import FileServiceInterface
from acutis_api.exception.errors.bad_request import HttpBadRequestError
from acutis_api.exception.errors.not_found import HttpNotFoundError


class RegistrarRecibosDoacaoAgapeUseCase:
    def __init__(
        self,
        agape_repository: AgapeRepositoryInterface,
        file_service: FileServiceInterface,
    ):
        self.agape_repository = agape_repository
        self.file_service = file_service

    def execute(
        self, doacao_id: uuid.UUID, dados: RegistrarRecibosRequestFormData
    ) -> None:
        doacao = self.agape_repository.buscar_doacao_agape_por_id(doacao_id)

        if not doacao:
            raise HttpNotFoundError(
                f'Doação com ID {doacao_id} não encontrada.'
            )

        for arquivo in dados.recibos:
            self.__valida_recibo(arquivo)

            self.agape_repository.registrar_foto_familia(
                FotoFamiliaAgapeSchema(
                    familia_id=doacao.fk_familia_agape_id,
                    foto=self.file_service.salvar_arquivo(arquivo),
                )
            )

        self.agape_repository.salvar_alteracoes()

    def __valida_recibo(self, recibo) -> None:
        if not recibo.filename:
            raise HttpBadRequestError('Nome do arquivo inválido.')

        extension = recibo.filename.rsplit('.', 1)[1].lower()

        allowed_extensions = {'png', 'jpg', 'jpeg'}
        if extension not in allowed_extensions:
            raise HttpBadRequestError('Extensão do arquivo não permitida.')
