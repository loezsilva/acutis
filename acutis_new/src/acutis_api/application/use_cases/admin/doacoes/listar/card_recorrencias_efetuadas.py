from datetime import datetime

from acutis_api.communication.requests.admin_doacoes import (
    CardsDoacoesRecorrentesResponse,
)
from acutis_api.domain.repositories.admin_doacoes import (
    AdminDoacoesRepositoryInterface,
)


class RecorrenciasEfetuadasUseCase:
    def __init__(self, repository: AdminDoacoesRepositoryInterface):
        self.__repository = repository

    def execute(self):
        data_inicio = datetime.now().replace(
            day=1, hour=0, minute=0, second=0, microsecond=0
        )
        data_fim = datetime.now()
        qtd_doacoes, total_doacoes = (
            self.__repository.contabilizar_recorrencias_efetuadas_periodo(
                data_inicio, data_fim
            )
        )

        return CardsDoacoesRecorrentesResponse(
            qtd_doacoes=qtd_doacoes, total=round(total_doacoes, 2)
        )
