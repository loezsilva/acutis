import uuid
from http import HTTPStatus

from acutis_api.communication.responses.agape import (
    CardTotalRecebimentosAgapeResponse,
)
from acutis_api.domain.repositories.agape import AgapeRepositoryInterface

# Assuming TotalItensRecebidosSchema will be defined here:
from acutis_api.domain.repositories.schemas.agape import (
    TotalItensRecebidosSchema,
)
from acutis_api.exception.errors.not_found import HttpNotFoundError


class CardTotalRecebimentosAgapeUseCase:
    def __init__(self, repository: AgapeRepositoryInterface):
        self.__repository = repository

    def execute(
        self, familia_id: uuid.UUID
    ) -> tuple[CardTotalRecebimentosAgapeResponse, HTTPStatus]:
        familia = self.__repository.buscar_familia_por_id(
            familia_id=familia_id
        )

        if familia is None:
            raise HttpNotFoundError('Família não encontrada.')

        dados_recebimentos: TotalItensRecebidosSchema = (
            self.__repository.total_itens_recebidos_por_familia(
                familia=familia
            )
        )

        total_itens = 0

        if dados_recebimentos and hasattr(
            dados_recebimentos, 'total_recebidas'
        ):
            total_itens = dados_recebimentos.total_recebidas

        response_data = CardTotalRecebimentosAgapeResponse(
            total_itens_recebidos=f'{total_itens} Itens recebidos'
        )

        return response_data, HTTPStatus.OK
