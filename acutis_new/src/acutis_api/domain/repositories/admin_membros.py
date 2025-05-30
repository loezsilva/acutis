import uuid
from abc import ABC, abstractmethod
from datetime import datetime

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

    @abstractmethod
    def excluir_conta(self, lead: Lead) -> None: ...

    @abstractmethod
    def buscar_total_leads(self) -> int: ...

    @abstractmethod
    def buscar_total_membros(self) -> int: ...

    @abstractmethod
    def buscar_leads_periodo(self, inicio: datetime, fim: datetime) -> int: ...

    @abstractmethod
    def buscar_membros_periodo(
        self, inicio: datetime, fim: datetime
    ) -> int: ...
