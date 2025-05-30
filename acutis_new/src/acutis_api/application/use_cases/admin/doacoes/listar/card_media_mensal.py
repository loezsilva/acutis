from datetime import datetime

from dateutil.relativedelta import relativedelta

from acutis_api.communication.requests.admin_doacoes import (
    CardMediaTotalResponse,
)
from acutis_api.domain.repositories.admin_doacoes import (
    AdminDoacoesRepositoryInterface,
)
from acutis_api.exception.errors.not_found import HttpNotFoundError


class MediaMensalUseCase:
    def __init__(self, repository: AdminDoacoesRepositoryInterface):
        self.__repository = repository

    def execute(self):
        soma_geral, primeira_doacao = self.__repository.soma_total_doacoes()

        if primeira_doacao is None:
            raise HttpNotFoundError('Nenhuma doação efetuada.')

        diferenca = relativedelta(datetime.now(), primeira_doacao[0])
        diferenca_meses = diferenca.years * 12 + diferenca.months

        media_mensal = (
            soma_geral / diferenca_meses if diferenca_meses != 0 else 1
        )

        return CardMediaTotalResponse(media=round(media_mensal, 2))
