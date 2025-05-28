import uuid

from acutis_api.communication.responses.admin_benfeitores import (
    BuscarInformacoesBenfeitorResponse,
)
from acutis_api.domain.repositories.admin_benfeitores import (
    AdminBenfeitoresRepositoryInterface,
)


class BuscarInformacoesBenfeitorUseCase:
    def __init__(self, repository: AdminBenfeitoresRepositoryInterface):
        self._repository = repository

    def execute(self, benfeitor_id: uuid.UUID):
        benfeitor = self._repository.buscar_informacoes_benfeitor_pelo_id(
            benfeitor_id
        )

        response = BuscarInformacoesBenfeitorResponse.model_validate(
            benfeitor
        ).model_dump()

        return response
