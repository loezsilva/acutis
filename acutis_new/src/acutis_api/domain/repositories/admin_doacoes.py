from abc import ABC, abstractmethod

from acutis_api.domain.repositories.schemas.admin_doacoes import (
    ListarDoacoesQuery,
    ListarDoacoesSchema,
)


class AdminDoacoesRepositoryInterface(ABC):
    @abstractmethod
    def listar_doacoes(
        self, filtros: ListarDoacoesQuery
    ) -> tuple[list[ListarDoacoesSchema], int]: ...
