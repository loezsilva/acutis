from datetime import datetime

from acutis_api.communication.requests.admin_doacoes import (
    CardMediaTotalResponse,
)
from acutis_api.domain.repositories.admin_doacoes import (
    AdminDoacoesRepositoryInterface,
)
from acutis_api.exception.errors.not_found import HttpNotFoundError


class MediaDiariaUseCase:
    def __init__(self, repository: AdminDoacoesRepositoryInterface):
        self.__repository = repository

    def execute(self):
        soma_geral, primeira_doacao = self.__repository.soma_total_doacoes()

        if primeira_doacao is None:
            raise HttpNotFoundError('Nenhuma doação efetuada.')

        diferenca_dias = (datetime.now() - primeira_doacao[0]).days

        media_diaria = (
            soma_geral / diferenca_dias if diferenca_dias != 0 else 1
        )

        return CardMediaTotalResponse(media=round(media_diaria, 2))
