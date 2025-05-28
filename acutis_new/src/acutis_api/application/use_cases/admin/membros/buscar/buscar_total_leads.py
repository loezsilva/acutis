from acutis_api.communication.responses.admin_membros import (
    BuscarTotalLeadsResponse,
)
from acutis_api.domain.repositories.admin_membros import (
    AdminMembrosRepositoryInterface,
)


class BuscarTotalLeadsUseCase:
    def __init__(self, repository: AdminMembrosRepositoryInterface):
        self._repository = repository

    def execute(self) -> dict:
        total_leads = self._repository.buscar_total_leads()
        response = BuscarTotalLeadsResponse(
            total_leads=total_leads
        ).model_dump()

        return response
