import uuid
from abc import ABC, abstractmethod
from typing import Any

from acutis_api.communication.requests.membros import (
    AtualizarDadosMembroRequest,
)
from acutis_api.domain.entities.campanha import Campanha
from acutis_api.domain.entities.doacao import Doacao
from acutis_api.domain.entities.endereco import Endereco
from acutis_api.domain.entities.lead import Lead
from acutis_api.domain.entities.lead_campanha import LeadCampanha
from acutis_api.domain.entities.membro import Membro
from acutis_api.domain.entities.metadado_lead import MetadadoLead
from acutis_api.domain.entities.oficial import Oficial
from acutis_api.domain.repositories.schemas.membros import (
    CampoAdicionalSchema,
    CardDoacoesMembroBenfeitorSchema,
    DoacaoMembroBenfeitorSchema,
    HistoricoDoacaoSchema,
    RegistrarNovoEnderecoSchema,
    RegistrarNovoLeadSchema,
    RegistrarNovoMembroSchema,
)
from acutis_api.domain.repositories.schemas.membros_oficiais import (
    RegistraMembroOficialSchema,
    RegistrarNovoMembroOficialResponse,
)
from acutis_api.domain.repositories.schemas.paginacao import PaginacaoQuery


class MembrosRepositoryInterface(ABC):
    @abstractmethod
    def salvar_alteracoes(self): ...

    @abstractmethod
    def verificar_cadastro_por_documento_e_email(
        self, documento: str, email: str
    ) -> Membro | None: ...

    @abstractmethod
    def buscar_lead_por_email(self, email: str) -> Lead | None: ...

    @abstractmethod
    def atualizar_dados_lead(
        self, lead: Lead, nome: str, email: str, telefone: str, pais: str
    ): ...

    @abstractmethod
    def ativa_conta_com_senha(senha_hashed: str, lead: Lead) -> None: ...

    @abstractmethod
    def registrar_novo_lead(self, dados: RegistrarNovoLeadSchema) -> Lead: ...

    @abstractmethod
    def registrar_novo_endereco(
        self, dados_endereco: RegistrarNovoEnderecoSchema
    ) -> Endereco: ...

    @abstractmethod
    def registrar_novo_membro(
        self,
        dados_membro: RegistrarNovoMembroSchema,
    ) -> Membro: ...

    @abstractmethod
    def buscar_membro_por_lead_id(self, id: uuid.UUID) -> Membro | None: ...

    @abstractmethod
    def buscar_campanha_por_id(self, id: uuid.UUID) -> Campanha | None: ...

    @abstractmethod
    def vincular_lead_a_campanha_registro(
        self, lead_id: uuid.UUID, campanha_id: uuid.UUID
    ): ...

    @abstractmethod
    def buscar_vinculo_de_lead_a_campanha_registro(
        self, lead_id: uuid.UUID, campanha_id: uuid.UUID
    ) -> LeadCampanha | None: ...

    @abstractmethod
    def registrar_campo_adicional_metadado_lead(
        self, lead_id: uuid.UUID, campo: CampoAdicionalSchema
    ): ...

    @abstractmethod
    def buscar_campo_adicional_metadado_lead(
        self, lead_id: uuid.UUID, campo_adicional_id: uuid.UUID
    ) -> MetadadoLead | None: ...

    @abstractmethod
    def atualizar_campo_adicional_metadado_lead(
        self, metadado_lead: MetadadoLead, valor_campo: Any
    ): ...

    @abstractmethod
    def buscar_lead_por_telefone(self, telefone: str) -> Lead | None: ...

    @abstractmethod
    def buscar_oficial_por_fk_membro_id(
        self, fk_membro_id: uuid.UUID
    ) -> Oficial: ...

    @abstractmethod
    def registrar_novo_membro_oficial(
        self, dados_da_requisicao: RegistraMembroOficialSchema
    ) -> RegistrarNovoMembroOficialResponse: ...

    @abstractmethod
    def alterar_senha(usuario: Lead, nova_senha: str): ...

    @abstractmethod
    def atualizar_data_ultimo_acesso(self, lead: Lead): ...

    @abstractmethod
    def excluir_conta(self, lead: Lead) -> None: ...

    @abstractmethod
    def remove_referencias_lead_id(self, fk_lead_id: uuid.UUID) -> None: ...

    @abstractmethod
    def listar_doacoes(
        self, filtros: PaginacaoQuery, benfeitor_id: uuid.UUID
    ) -> tuple[list[DoacaoMembroBenfeitorSchema], int]: ...

    @abstractmethod
    def buscar_doacao_por_id(self, id: uuid.UUID) -> Doacao | None: ...

    @abstractmethod
    def buscar_historico_doacao_por_doacao_id(
        self, filtros: PaginacaoQuery, id: uuid.UUID
    ) -> tuple[list[HistoricoDoacaoSchema], int]: ...

    @abstractmethod
    def atualizar_dados_membro(
        self, request: AtualizarDadosMembroRequest, membro: Membro
    ): ...

    @abstractmethod
    def buscar_card_doacoes_membro_benfeitor(
        self, benfeitor_id: uuid.UUID
    ) -> CardDoacoesMembroBenfeitorSchema: ...
