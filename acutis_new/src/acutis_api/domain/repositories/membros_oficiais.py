import uuid
from abc import ABC, abstractmethod

from acutis_api.domain.entities.cargo_oficial import CargosOficiais
from acutis_api.domain.entities.membro import Membro
from acutis_api.domain.entities.oficial import Oficial
from acutis_api.domain.repositories.enums.membros_oficiais import (
    StatusMembroOficialEnum,
)
from acutis_api.domain.repositories.schemas.admin_membros_oficiais import (
    AlterarCargoOficialSchema,
    ListarMembrosOficiaisSchema,
)
from acutis_api.domain.repositories.schemas.membros_oficiais import (
    RegistraMembroOficialSchema,
    RegistrarNovoMembroOficialResponse,
)


class MembrosOficiaisRepositoryInterface(ABC):
    @abstractmethod
    def registrar_novo_membro_oficial(
        self, dados_da_requisicao: RegistraMembroOficialSchema
    ) -> RegistrarNovoMembroOficialResponse: ...

    @abstractmethod
    def buscar_oficial_por_fk_membro_id(
        self, fk_membro_id: uuid.UUID
    ) -> Oficial: ...

    @abstractmethod
    def salvar_dados(self): ...

    @abstractmethod
    def admin_listar_membros_oficiais(
        self, filtros_da_requisicao: ListarMembrosOficiaisSchema
    ) -> tuple: ...

    @abstractmethod
    def busca_nome_de_usuario_superior(
        self, fk_usuario_superior_id: uuid.UUID
    ) -> str: ...

    @abstractmethod
    def buscar_nome_cargo_oficial(self, fk_cargo_oficial_id) -> str: ...

    @abstractmethod
    def buscar_membro_oficial_por_id(
        self, fk__membro_oficial_id: uuid.UUID
    ) -> Oficial: ...

    @abstractmethod
    def atualizar_status_membro_oficial(
        self,
        membro_oficial_para_atualizar: Oficial,
        status: StatusMembroOficialEnum,
    ) -> Oficial: ...

    @abstractmethod
    def busca_cargo_oficial_por_id(
        self, fk_cargo_oficial_id: uuid.UUID
    ) -> CargosOficiais: ...

    @abstractmethod
    def admin_alterar_cargo_oficial(
        membro_oficial: Oficial, requisicao: AlterarCargoOficialSchema
    ) -> Oficial: ...

    @abstractmethod
    def remover_vinculos_de_superior(
        self, fk_membro_oficial_id: uuid.UUID = None
    ) -> None: ...

    @abstractmethod
    def admin_excluir_oficial(self, oficial_para_deletar: Oficial) -> None: ...

    @abstractmethod
    def busca_membro_por_id(self, fk_membro_id: uuid.UUID) -> Membro: ...

    @abstractmethod
    def busca_superiores_de_cargo_oficial(
        self, fk_cargo_oficial_id: uuid.UUID
    ) -> Oficial: ...
