import uuid
from abc import ABC, abstractmethod
from uuid import UUID

from acutis_api.domain.entities.campanha import Campanha
from acutis_api.domain.entities.campanha_doacao import CampanhaDoacao
from acutis_api.domain.entities.landing_page import LandingPage
from acutis_api.domain.repositories.schemas.campanhas import (
    ListarCampanhasQuery,
    ListarDoacoesCampanhaSchema,
    RegistrarCampanhaSchema,
    RegistrarNovaLandingPageSchema,
    RegistroNovoCampoAdicionalSchema,
)
from acutis_api.domain.repositories.schemas.paginacao import PaginacaoQuery


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
    ) -> Campanha: ...

    @abstractmethod
    def buscar_campanha_por_id(self, fk_campanha_id: UUID) -> Campanha: ...

    @abstractmethod
    def buscar_campanha_por_nome(self, nome_campanha: str) -> Campanha: ...

    @abstractmethod
    def lista_de_campanhas(self) -> Campanha: ...

    @abstractmethod
    def buscar_landing_page_por_campanha_id(
        self, fk_campanha_id: uuid.UUID
    ) -> LandingPage: ...

    @abstractmethod
    def buscar_landing_page_por_id(
        self, landing_page_id: uuid.UUID
    ) -> LandingPage: ...

    @abstractmethod
    def listar_doacoes_campanha_pelo_id(
        self, filtros: PaginacaoQuery, id: uuid.UUID
    ) -> tuple[list[ListarDoacoesCampanhaSchema], int]: ...

    @abstractmethod
    def registrar_campanha_doacao(
        self, chave_pix: str, campanha_id: uuid.UUID
    ): ...

    @abstractmethod
    def atualizar_campanha_doacao(
        self, chave_pix: str, campanha_doacao: CampanhaDoacao
    ): ...
