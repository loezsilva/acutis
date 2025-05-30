from datetime import datetime

from dateutil.relativedelta import relativedelta

from acutis_api.communication.requests.admin_doacoes import (
    CardDoacoesTotalResponse,
)
from acutis_api.domain.repositories.admin_doacoes import (
    AdminDoacoesRepositoryInterface,
)
from acutis_api.exception.errors.not_found import HttpNotFoundError


class CardDoacoesDoMesUseCase:
    def __init__(self, repository: AdminDoacoesRepositoryInterface):
        self.__repository = repository

    def execute(self):
        total_mes, primeira_doacao, soma_geral, quantidade_mes = (
            self.__repository.card_doacoes_mes_atual()
        )

        if primeira_doacao is None:
            raise HttpNotFoundError('Nenhuma doação efetuada.')

        diferenca = relativedelta(datetime.now(), primeira_doacao[0])
        diferenca_meses = diferenca.years * 12 + diferenca.months

        media_mensal = (
            soma_geral / diferenca_meses if diferenca_meses != 0 else 1
        )

        porcentagem = ((total_mes - media_mensal) / media_mensal) * 100

        return CardDoacoesTotalResponse(
            total=total_mes,
            porcentagem=round(porcentagem, 2),
            quantidade=quantidade_mes,
        )
