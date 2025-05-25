import uuid
from abc import ABC, abstractmethod

from acutis_api.domain.entities.lead import Lead
from acutis_api.domain.repositories.schemas.admin_membros import (
    ListarLeadsMembrosFiltros,
    ListarLeadsMembrosSchema,
)


class AdminMembrosRepositoryInterface(ABC):
    @abstractmethod
    def listar_leads_e_membros(
        self, filtros: ListarLeadsMembrosFiltros
    ) -> tuple[list[ListarLeadsMembrosSchema], int]: ...

    @abstractmethod
    def buscar_lead_por_id(self, id: uuid.UUID) -> Lead | None: ...
