from acutis_api.domain.repositories.enderecos import (
    EnderecosRepositoryInterface,
)
from acutis_api.exception.errors.not_found import HttpNotFoundError


class BuscarCepUseCase:
    def __init__(self, repository: EnderecosRepositoryInterface):
        self._repository = repository

    def execute(self, cep: str):
        cep = cep.replace('-', '')
        endereco = self._repository.buscar_cep(cep)
        if endereco is None:
            raise HttpNotFoundError('CEP não encontrado na base de dados.')

        return endereco
