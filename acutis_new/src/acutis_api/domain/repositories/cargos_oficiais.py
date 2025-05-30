import uuid
from abc import ABC, abstractmethod

from acutis_api.domain.entities.cargo_oficial import CargosOficiais
from acutis_api.domain.repositories.schemas.cargos_oficiais import (
    ListarCargosOficiaisSchema,
)


class CargosOficiaisRepositoryInterface(ABC):
    @abstractmethod
    def salvar_dados(self) -> None: ...

    @abstractmethod
    def busca_cargo_por_nome(self, nome: str) -> CargosOficiais: ...

    @abstractmethod
    def registrar_novo_cargo_vocacional(
        self, nome_cargo: str, fk_cargo_superior_id: uuid.UUID
    ) -> CargosOficiais: ...

    @abstractmethod
    def listar_todos_cargos_oficiais(
        self, filtros: ListarCargosOficiaisSchema
    ) -> ListarCargosOficiaisSchema: ...

    @abstractmethod
    def busca_cargo_oficial_por_id(
        self, fk_cargo_oficial_id: uuid.UUID
    ) -> CargosOficiais: ...

    @abstractmethod
    def atualizar_cargo_oficial(
        self, cargo_para_atualizar: CargosOficiais, dados_para_atualizar: dict
    ) -> CargosOficiais: ...

    @abstractmethod
    def buscar_oficiais_com_cargo_a_ser_deletado(
        self, fk_cargo_id: uuid.UUID
    ) -> None: ...

    @abstractmethod
    def admin_deleta_cargo_oficial(self, fk_cargo_id: uuid.UUID) -> None: ...

    @abstractmethod
    def lista_de_cargos_oficiais(self) -> CargosOficiais: ...

    @abstractmethod
    def obter_total_cadastros_cargo_oficial(self): ...
