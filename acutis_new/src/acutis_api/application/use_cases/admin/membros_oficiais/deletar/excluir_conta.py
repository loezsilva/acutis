from acutis_api.domain.repositories.admin_membros import (
    AdminMembrosRepositoryInterface,
)
from acutis_api.exception.errors.not_found import HttpNotFoundError


class AdminExcluirContaUseCase:
    def __init__(self, repository: AdminMembrosRepositoryInterface):
        self.__repository = repository

    def execute(self, uuid: str) -> None:
        lead = self.__repository.buscar_lead_por_id(uuid)
        if not lead:
            raise HttpNotFoundError('Usuário não encontrado.')

        self.__repository.excluir_conta(lead)
