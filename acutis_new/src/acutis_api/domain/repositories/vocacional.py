from abc import ABC, abstractmethod
from uuid import UUID

from flask_sqlalchemy.pagination import Pagination

from acutis_api.domain.entities.cadastro_vocacional import CadastroVocacional
from acutis_api.domain.entities.etapa_vocacional import EtapaVocacional
from acutis_api.domain.entities.ficha_vocacional import FichaVocacional
from acutis_api.domain.entities.sacramento_vocacional import (
    SacramentoVocacional,
)
from acutis_api.domain.entities.usuario_vocacional import UsuarioVocacional
from acutis_api.domain.repositories.schemas.vocacional import (
    DecodificarTokenVocacionalSchema,
    ListarCadastrosVocacionaisSchema,
    ListarDesistenciaVocacionaisSchema,
    ListarFichasVocacionaisSchema,
    ListarPreCadastrosSchema,
    ListarVocacionaisRecusadosSchema,
    RegistrarCadastroVocacionalSchema,
    RegistrarPreCadastroSchema,
)


class InterfaceVocacionalRepository(ABC):  # noqa: PLR0904
    @abstractmethod
    def salvar_alteracoes(self): ...

    @abstractmethod
    def deletar_vocacional(
        self, fk_usuario_vocacional_id: UsuarioVocacional
    ): ...

    @abstractmethod
    def verificar_usuario_vocacional_por_email(
        self, data: dict
    ) -> CadastroVocacional | None: ...

    @abstractmethod
    def pre_cadastro_vocacional(
        self, data_request: RegistrarPreCadastroSchema
    ) -> UsuarioVocacional | None: ...

    @abstractmethod
    def busca_pre_cadastro_vocacional(
        self, filters: ListarPreCadastrosSchema
    ) -> Pagination: ...

    @abstractmethod
    def detalhes_da_etapa_vocacional(
        self,
        etapa_vocacional: str,
        fk_usuario_vocacional_id: UUID,
    ) -> EtapaVocacional | None: ...

    @abstractmethod
    def busca_etapa_atual(
        self, fk_usuario_vocacional_id: UUID
    ) -> EtapaVocacional | None: ...

    @abstractmethod
    def busca_sacramento_vocacional(
        self, ficha_vocacional_id: UUID
    ) -> list[SacramentoVocacional]: ...

    @abstractmethod
    def verifica_usuario_vocacional(
        self, fk_usuario_vocacional_id: UUID
    ) -> UsuarioVocacional | None: ...

    @abstractmethod
    def busca_vocacional(
        self, fk_usuario_vocacional_id: UUID
    ) -> EtapaVocacional | None: ...

    @abstractmethod
    def aprovar_para_proximo_passo(self, fk_usuario_vocacional_id: UUID): ...

    @abstractmethod
    def reprovar_para_proximo_passo(
        self, fk_usuario_vocacional_id: UUID, justificativa: str | None
    ): ...

    @abstractmethod
    def registrar_desistencia(
        self, fk_usuario_vocacional_id: UUID, etapa: EtapaVocacional
    ): ...

    @abstractmethod
    def busca_etapa_vocacional_por_usuario_e_etapa(
        self, fk_usuario_vocacional_id: UUID, etapa: str
    ) -> EtapaVocacional | None: ...

    @abstractmethod
    def verifica_cadastro_vocacional(
        self, fk_usuario_vocacional_id: UUID
    ) -> CadastroVocacional | None: ...

    @abstractmethod
    def verifica_cpf_cadastrado(
        self, documento_identidade: str
    ) -> CadastroVocacional | None: ...

    @abstractmethod
    def registrar_cadastro_vocacional(
        self, data: RegistrarCadastroVocacionalSchema
    ) -> CadastroVocacional: ...

    @abstractmethod
    def buscar_cadastros_vocacional(
        self, filters: ListarCadastrosVocacionaisSchema
    ) -> Pagination: ...

    @abstractmethod
    def verifica_ficha_vocacional(
        self, usuario_vocacional_id: UUID
    ) -> FichaVocacional | None: ...

    @abstractmethod
    def registrar_ficha_vocacional(self, data: dict): ...

    @abstractmethod
    def buscar_fichas_vocacionais(
        self, filters: ListarFichasVocacionaisSchema
    ) -> Pagination: ...

    @abstractmethod
    def buscar_desistencias_vocacionais(
        self, filters: ListarDesistenciaVocacionaisSchema
    ) -> Pagination: ...

    @abstractmethod
    def buscar_vocacionais_recusados(
        self, filters: ListarVocacionaisRecusadosSchema
    ) -> Pagination: ...

    @abstractmethod
    def busca_responsavel_atualizou_status(
        self, fk_usuario_atualizou_status_id: UUID, etapa: str
    ) -> str | None: ...

    @abstractmethod
    def busca_info_token(
        self, data_decode_token
    ) -> DecodificarTokenVocacionalSchema | None: ...
