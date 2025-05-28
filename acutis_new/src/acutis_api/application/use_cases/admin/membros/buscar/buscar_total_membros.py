from acutis_api.communication.responses.admin_membros import (
    BuscarTotalMembrosResponse,
)
from acutis_api.domain.repositories.admin_membros import (
    AdminMembrosRepositoryInterface,
)


class BuscarTotalMembrosUseCase:
    def __init__(self, repository: AdminMembrosRepositoryInterface):
        self._repository = repository

    def execute(self) -> dict:
        total_membros = self._repository.buscar_total_membros()
        response = BuscarTotalMembrosResponse(
            total_membros=total_membros
        ).model_dump()

        return response
