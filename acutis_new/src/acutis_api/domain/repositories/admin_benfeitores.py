import uuid
from abc import ABC, abstractmethod
from datetime import date

from acutis_api.domain.repositories.schemas.admin_benfeitores import (
    BuscarCardsDoacoesBenfeitoresSchema,
    BuscarInformacoesBenfeitorSchema,
    ListarBenfeitoresFiltros,
    ListarBenfeitoresSchema,
    ListarDoacoesAnonimasBenfeitorSchema,
)
from acutis_api.domain.repositories.schemas.paginacao import PaginacaoQuery


class AdminBenfeitoresRepositoryInterface(ABC):
    @abstractmethod
    def buscar_cards_doacoes_benfeitores(
        self,
        mes_atual_inicio: date,
        mes_atual_final: date,
        mes_anterior_inicio: date,
        mes_anterior_final: date,
    ) -> BuscarCardsDoacoesBenfeitoresSchema: ...

    @abstractmethod
    def listar_benfeitores(
        self,
        filtros: ListarBenfeitoresFiltros,
    ) -> tuple[list[ListarBenfeitoresSchema], int]: ...

    @abstractmethod
    def buscar_informacoes_benfeitor_pelo_id(
        self, id: uuid.UUID
    ) -> BuscarInformacoesBenfeitorSchema: ...

    @abstractmethod
    def listar_doacoes_anonimas_benfeitor_pelo_id(
        self, filtros: PaginacaoQuery, id: uuid.UUID
    ) -> tuple[list[ListarDoacoesAnonimasBenfeitorSchema], int]: ...
