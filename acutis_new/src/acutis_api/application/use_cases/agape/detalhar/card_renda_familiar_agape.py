import uuid

from acutis_api.communication.responses.agape import (
    CardRendaFamiliarAgapeResponse,
)
from acutis_api.domain.repositories.agape import AgapeRepositoryInterface
from acutis_api.exception.errors.not_found import HttpNotFoundError

SALARIO_MINIMO = 1518.0


class CardRendaFamiliarAgapeUseCase:
    def __init__(self, repository: AgapeRepositoryInterface):
        self.__repository = repository

    def execute(self, familia_id: uuid.UUID) -> CardRendaFamiliarAgapeResponse:
        familia = self.__repository.buscar_familia_por_id(familia_id)

        if not familia:
            raise HttpNotFoundError(
                f'Família com ID {familia_id} não encontrada ou foi deletada.'
            )

        quantidade_membros_familia = (
            self.__repository.numero_membros_familia_agape(familia_id)
        )

        renda_familiar_data = self.__repository.soma_renda_familiar_agape(
            familia
        )

        soma_renda = getattr(renda_familiar_data, 'total', 0.0)

        renda_per_capita_soma = 0.0
        renda_total_soma = 0.0

        if soma_renda > 0:
            renda_total_soma = soma_renda / SALARIO_MINIMO
            if quantidade_membros_familia > 0:
                renda_per_capita_soma = (
                    soma_renda / quantidade_membros_familia
                ) / SALARIO_MINIMO

        return CardRendaFamiliarAgapeResponse(
            renda_familiar=f'{renda_total_soma:.1f} Salários mínimos',
            renda_per_capta=f'{renda_per_capita_soma:.1f} Salários mínimos',
        ).model_dump()
