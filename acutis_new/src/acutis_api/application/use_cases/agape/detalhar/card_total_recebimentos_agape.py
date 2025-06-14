import uuid

from acutis_api.communication.responses.agape import (
    CardTotalRecebimentosAgapeResponse,
)
from acutis_api.domain.repositories.agape import AgapeRepositoryInterface
from acutis_api.exception.errors.not_found import HttpNotFoundError


class CardTotalRecebimentosAgapeUseCase:
    def __init__(self, repository: AgapeRepositoryInterface):
        self.__repository = repository

    def execute(
        self, familia_id: uuid.UUID
    ) -> CardTotalRecebimentosAgapeResponse:
        familia = self.__repository.buscar_familia_por_id(
            familia_id=familia_id
        )

        if familia is None:
            raise HttpNotFoundError('Família não encontrada.')

        total_itens_recebidos = (
            self.__repository.total_itens_recebidos_por_familia(
                familia=familia
            )
        )

        return CardTotalRecebimentosAgapeResponse(
            total_itens_recebidos=f'{total_itens_recebidos} Itens recebidos'
        ).model_dump()
