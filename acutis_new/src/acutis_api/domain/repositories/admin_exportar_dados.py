import uuid
from abc import ABC, abstractmethod

from acutis_api.domain.entities.lead import Lead
from acutis_api.domain.repositories.schemas.admin_exportar_dados import (
    ExportarBenfeitoresSchema,
    ExportarDoacoesSchema,
    ExportarMembrosSchema,
    ExportMembrosOficiaisSchema,
)


class ExportarDadosRepositoryInterface(ABC):
    @abstractmethod
    def exportar_leads(self, colunas, filtros) -> Lead: ...

    @abstractmethod
    def exportar_membros(self, colunas, requisicao: ExportarMembrosSchema): ...

    @abstractmethod
    def exportar_membros_oficiais(
        self, colunas, requisicao: ExportMembrosOficiaisSchema
    ): ...

    @abstractmethod
    def buscar_nome_usuario_superior(self, id: uuid.UUID) -> Lead | None: ...

    @abstractmethod
    def buscar_nome_cargo_oficial(
        self, cargo_oficial_id: uuid.UUID
    ) -> str | None: ...

    @abstractmethod
    def exportar_doacoes(  # NOSONAR
        self, colunas, request: ExportarDoacoesSchema
    ): ...

    @abstractmethod
    def exportar_benfeitores(
        self, colunas, request: ExportarBenfeitoresSchema
    ): ...
