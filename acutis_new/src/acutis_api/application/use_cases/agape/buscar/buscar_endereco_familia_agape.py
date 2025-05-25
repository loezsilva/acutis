from uuid import UUID
from acutis_api.domain.repositories.agape import AgapeRepositoryInterface
from acutis_api.communication.responses.agape import EnderecoResponse
from acutis_api.exception.errors.not_found import HttpNotFoundError

class BuscarEnderecoFamiliaAgapeUseCase:
    def __init__(self, agape_repository: AgapeRepositoryInterface):
        self._agape_repository = agape_repository

    def execute(self, familia_id: UUID) -> EnderecoResponse:
        familia_agape_entity = self._agape_repository.buscar_familia_agape_por_id(familia_id)
        if not familia_agape_entity.fk_endereco_id:
            raise HttpNotFoundError(f"Família ágape {familia_id} não possui endereço associado.")
        endereco_entity = self._agape_repository.buscar_endereco_por_id(familia_agape_entity.fk_endereco_id)
        return EnderecoResponse.model_validate(endereco_entity)
