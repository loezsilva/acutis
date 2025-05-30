from datetime import datetime

from acutis_api.communication.requests.admin_doacoes import (
    CardDoacoesTotalResponse,
)
from acutis_api.domain.repositories.admin_doacoes import (
    AdminDoacoesRepositoryInterface,
)
from acutis_api.exception.errors.not_found import HttpNotFoundError


class CardDoacoesDoDiaUseCase:
    def __init__(self, repository: AdminDoacoesRepositoryInterface):
        self.__repository = repository

    def execute(self):
        total_hoje, primeira_doacao, soma_geral, quantidade_hoje = (
            self.__repository.card_doacoes_dia_atual()
        )

        if primeira_doacao is None:
            raise HttpNotFoundError('Nenhuma doação efetuada.')

        diferenca_dias = (datetime.now() - primeira_doacao[0]).days

        media_diaria = (
            soma_geral / diferenca_dias if diferenca_dias != 0 else 1
        )

        porcentagem = ((total_hoje - media_diaria) / media_diaria) * 100

        return CardDoacoesTotalResponse(
            total=total_hoje,
            porcentagem=round(porcentagem, 2),
            quantidade=quantidade_hoje,
        )
