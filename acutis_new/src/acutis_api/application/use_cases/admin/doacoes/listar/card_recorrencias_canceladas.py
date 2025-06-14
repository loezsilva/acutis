from acutis_api.communication.requests.admin_doacoes import (
    CardsDoacoesRecorrentesResponse,
)
from acutis_api.domain.repositories.admin_doacoes import (
    AdminDoacoesRepositoryInterface,
)


class RecorrenciasCanceladasUseCase:
    def __init__(self, repository: AdminDoacoesRepositoryInterface):
        self.__repository = repository

    def execute(self):
        qtd_doacoes, total_doacoes = (
            self.__repository.contabilizar_recorrencias_canceladas()
        )

        return CardsDoacoesRecorrentesResponse(
            qtd_doacoes=qtd_doacoes,
            total=round(total_doacoes, 2),
        )
