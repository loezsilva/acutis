from acutis_api.communication.requests.admin_doacoes import (
    CardRecorrentesComDoadoresResponse,
)
from acutis_api.domain.repositories.admin_doacoes import (
    AdminDoacoesRepositoryInterface,
)


class RecorrenciasLembretesEfetivosUseCase:
    def __init__(self, repository: AdminDoacoesRepositoryInterface):
        self.__repository = repository

    def execute(self):
        qtd_doacoes, total_doacoes, qtd_doadores = (
            self.__repository.contabilizar_lembretes_efetivos()
        )

        return CardRecorrentesComDoadoresResponse(
            qtd_doacoes=qtd_doacoes,
            total=round(total_doacoes, 2),
            qtd_doadores=qtd_doadores,
        )
