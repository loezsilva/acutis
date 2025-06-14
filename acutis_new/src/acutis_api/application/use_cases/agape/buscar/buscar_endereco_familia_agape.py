from uuid import UUID

from acutis_api.communication.responses.agape import (
    EnderecoComCoordenadasResponse,
)
from acutis_api.domain.repositories.agape import AgapeRepositoryInterface
from acutis_api.exception.errors.not_found import HttpNotFoundError


class BuscarEnderecoFamiliaAgapeUseCase:
    def __init__(self, agape_repository: AgapeRepositoryInterface):
        self._agape_repository = agape_repository

    def execute(self, familia_id: UUID) -> EnderecoComCoordenadasResponse:
        familia_agape = self._agape_repository.buscar_familia_por_id(
            familia_id
        )

        if familia_agape is None:
            raise HttpNotFoundError(
                f'Família ágape {familia_id} não encontrada.'
            )

        endereco_familia = self._agape_repository.buscar_endereco_por_id(
            familia_agape.fk_endereco_id
        )

        endereco_response = EnderecoComCoordenadasResponse.model_validate(
            endereco_familia
        ).model_dump()

        if endereco_familia.coordenada:
            endereco_response['latitude'] = (
                endereco_familia.coordenada.latitude
            )
            endereco_response['longitude'] = (
                endereco_familia.coordenada.longitude
            )

        return endereco_response
