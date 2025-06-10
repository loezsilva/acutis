import uuid

from acutis_api.communication.responses.agape import (
    CardRendaFamiliarAgapeResponse,
)
from acutis_api.domain.repositories.agape import AgapeRepositoryInterface
from acutis_api.exception.errors.not_found import HttpNotFoundError

SALARIO_MINIMO = 1518.0  # Defined as float for division


class CardRendaFamiliarAgapeUseCase:
    def __init__(self, repository: AgapeRepositoryInterface):
        self.__repository = repository

    def execute(self, familia_id: uuid.UUID) -> CardRendaFamiliarAgapeResponse:
        familia = self.__repository.buscar_familia_por_id(familia_id)
        if not familia:
            raise HttpNotFoundError(
                f'Família com ID {familia_id} não encontrada ou foi deletada.'
            )

        membros_count_data = self.__repository.numero_membros_familia_agape(
            familia_id
        )

        numero_membros = getattr(membros_count_data, 'quantidade', 0)

        renda_familiar_data = self.__repository.soma_renda_familiar_agape(
            familia
        )

        soma_renda = getattr(renda_familiar_data, 'total', 0.0)

        renda_per_capita_sm = 0.0
        renda_total_sm = 0.0

        if soma_renda > 0:
            renda_total_sm = soma_renda / SALARIO_MINIMO
            if numero_membros > 0:
                renda_per_capita_sm = (
                    soma_renda / numero_membros
                ) / SALARIO_MINIMO

        return CardRendaFamiliarAgapeResponse(
            renda_familiar=f'{renda_total_sm:.1f} Salários mínimos',
            renda_per_capta=f'{renda_per_capita_sm:.1f} Salários mínimos',
        ).model_dump()
