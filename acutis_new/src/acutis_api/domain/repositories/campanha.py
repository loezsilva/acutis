from abc import ABC, abstractmethod
from uuid import UUID

from acutis_api.domain.entities.campanha import Campanha
from acutis_api.domain.repositories.schemas.campanhas import (
    ListarCampanhasQuery,
    RegistrarCampanhaSchema,
    RegistrarNovaLandingPageSchema,
    RegistroNovoCampoAdicionalSchema,
)


class CampanhaRepositoryInterface(ABC):
    @abstractmethod
    def registrar_nova_campanha(
        self, dados_da_requiscao: RegistrarCampanhaSchema
    ) -> None: ...

    @abstractmethod
    def salvar_alteracoes(self) -> None: ...

    @abstractmethod
    def verificar_nome_da_campanha(self, nome_campanha: str) -> tuple: ...

    @abstractmethod
    def listar_campanhas(
        self, filtros_da_requisicao: ListarCampanhasQuery
    ) -> dict: ...

    @abstractmethod
    def atualizar_landing_page(
        self,
        landing_page,
        dados_da_landing_page: RegistrarNovaLandingPageSchema,
    ) -> dict: ...

    @abstractmethod
    def criar_landing_page(
        self,
        fk_campanha_id: UUID,
        dados_da_landing_page: RegistrarNovaLandingPageSchema,
    ) -> dict: ...

    @abstractmethod
    def atualizar_campos_adicionais(
        self,
        campos_adicionais_consulta,
        dados_campos_adicionais: RegistroNovoCampoAdicionalSchema,
    ) -> dict: ...

    @abstractmethod
    def criar_campos_adicionais(
        self,
        fk_campanha_id: UUID,
        dados_campos_adicionais: RegistroNovoCampoAdicionalSchema,
    ) -> dict: ...

    @abstractmethod
    def buscar_campos_adicionais(self, fk_campanha_id: int) -> dict: ...

    @abstractmethod
    def atualizar_campanha(
        self,
        campanha_para_atualizar: Campanha,
        dados_da_campanha: RegistrarCampanhaSchema,
    ) -> None: ...

    @abstractmethod
    def buscar_campanha_por_id(self, fk_campanha_id: UUID) -> Campanha: ...

    @abstractmethod
    def buscar_campanha_por_nome(self, nome_campanha: str) -> Campanha: ...

    @abstractmethod
    def lista_de_campanhas(self) -> Campanha: ...
