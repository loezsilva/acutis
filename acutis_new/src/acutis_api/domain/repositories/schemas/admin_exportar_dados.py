import uuid
from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field

from acutis_api.communication.enums.membros_oficiais import StatusOficialEnum
from acutis_api.domain.entities.membro import SexoEnum
from acutis_api.domain.entities.pagamento_doacao import (
    FormaPagamentoEnum,
    GatewayPagamentoEnum,
)
from acutis_api.domain.entities.processamento_doacao import (
    StatusProcessamentoEnum,
)
from acutis_api.domain.repositories.enums.admin_exportar_dados import (
    ExportarBenfeitoresEnum,
    ExportarDoacoesEnum,
)


class ExportaLeadsSchema(BaseModel):
    colunas: str = Field(
        ...,
        description="['id', 'nome', 'email', 'status', 'telefone', \
        'origem_cadastro', 'criado_em', 'ultimo_acesso', 'pais']",
    )
    id: Optional[uuid.UUID] = None
    telefone: Optional[str] = None
    pais: Optional[str] = None
    nome: Optional[str] = None
    status: Optional[StatusOficialEnum] = None
    origem_cadastro: Optional[uuid.UUID] = None
    data_inicio: Optional[date] = None
    data_fim: Optional[date] = None
    email: Optional[str] = None


class ExportarMembrosSchema(ExportaLeadsSchema):
    colunas: str = Field(
        ...,
        description="['id', 'nome', 'email', 'status', 'telefone', \
        'origem_cadastro', 'criado_em', 'ultimo_acesso', \
        'pais', 'numero_documento', 'fk_lead_id', sexo]",
    )
    numero_documento: Optional[str] = None
    sexo: Optional[SexoEnum] = None
    fk_lead_id: Optional[uuid.UUID] = None


class ExportMembrosOficiaisSchema(ExportarMembrosSchema):
    colunas: str = Field(
        ...,
        description="['id', 'nome', 'email', 'status', 'sexo', 'telefone', \
        'criado_em','numero_documento', 'fk_membro_id', 'atualizado_por', \
        'atualizado_por', 'fk_superior_id', 'fk_cargo_oficial_id']",
    )
    fk_superior_id: Optional[uuid.UUID] = None
    atualizado_por: Optional[uuid.UUID] = None
    fk_cargo_oficial_id: Optional[uuid.UUID] = None


class ExportarDoacoesSchema(BaseModel):  # NOSONAR
    colunas: list[ExportarDoacoesEnum]
    nome_email_documento: str | None = None
    campanha_id: uuid.UUID | None = None
    campanha_nome: str | None = None
    data_doacao_cancelada_em_inicial: date | None = None
    data_doacao_cancelada_em_final: date = Field(
        default_factory=lambda: datetime.now().date()
    )
    data_doacao_criada_em_inicial: date | None = None
    data_doacao_criada_em_final: date = Field(
        default_factory=lambda: datetime.now().date()
    )
    recorrente: bool = None  # NOSONAR
    forma_pagamento: FormaPagamentoEnum = None  # NOSONAR
    codigo_ordem_pagamento: str | None = None
    anonimo: bool = None  # NOSONAR
    gateway: GatewayPagamentoEnum = None  # NOSONAR
    ativo: bool = None  # NOSONAR
    doacao_processada_em_inicial: date | None = None
    doacao_processada_em_final: date = Field(
        default_factory=lambda: datetime.now().date()
    )
    codigo_transacao: str | None = None
    codigo_comprovante: str | None = None
    nosso_numero: str | None = None
    status: StatusProcessamentoEnum = None  # NOSONAR


class ExportarBenfeitoresSchema(BaseModel):
    colunas: list[ExportarBenfeitoresEnum]
    nome_documento: str | None = None
    campanha_id: uuid.UUID | None = None
    campanha_nome: str | None = None
    registrado_em_inicio: date | None = None
    registrado_em_fim: date = datetime.now().date()
    ultima_doacao_inicio: date | None = None
    ultima_doacao_fim: date = datetime.now().date()
