import uuid
from datetime import datetime
from types import NoneType
from typing import Any

from pydantic import BaseModel, ConfigDict, EmailStr, field_validator

from acutis_api.communication.enums.membros import SexoEnum
from acutis_api.communication.responses.padrao import PaginacaoResponse


class LeadsMembrosSchema(BaseModel):
    lead_id: uuid.UUID
    nome: str
    email: str
    telefone: str | None
    pais: str | None
    data_cadastro_lead: str
    lead_atualizado_em: str
    membro_id: uuid.UUID | None
    benfeitor_id: uuid.UUID | None
    endereco_id: uuid.UUID | None
    nome_social: str | None
    data_nascimento: str | None
    numero_documento: str | None
    sexo: SexoEnum | None
    foto: str | None
    ultimo_acesso: str | None
    status_conta_lead: bool | None
    data_cadastro_membro: str | None
    membro_atualizado_em: str | None
    cadastro_membro_atualizado_em: str | None


class ListarLeadsMembrosResponse(PaginacaoResponse):
    leads_e_membros: list[LeadsMembrosSchema]


class LeadSchema(BaseModel):
    id: uuid.UUID
    nome: str
    email: EmailStr
    telefone: str
    pais: str
    status: bool
    data_cadastro: datetime | str
    ultimo_acesso: datetime | str | None

    @field_validator('data_cadastro', 'ultimo_acesso')
    @classmethod
    def formatar_datetime(cls, value: datetime):
        if isinstance(value, (str, NoneType)):
            return value

        return value.strftime('%d/%m/%Y %H:%M')


class MembroSchema(BaseModel):
    id: uuid.UUID | None
    foto: str | None
    numero_documento: str | None
    nome_social: str | None


class EnderecoSchema(BaseModel):
    id: uuid.UUID | None
    cep: str | None
    tipo_logradouro: str | None
    logradouro: str | None
    numero: str | None
    complemento: str | None
    bairro: str | None
    cidade: str | None
    estado: str | None
    pais: str | None


class CampanhasRegistradasSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    nome: str | None
    campos_adicionais: list[dict[str, Any]]


class BuscarDetalhesDoLeadResponse(BaseModel):
    dados_lead: LeadSchema
    dados_membro: MembroSchema | None
    dados_endereco: EnderecoSchema | None
    campanhas_registradas: list[CampanhasRegistradasSchema]


class BuscarTotalLeadsResponse(BaseModel):
    total_leads: int


class BuscarTotalMembrosResponse(BaseModel):
    total_membros: int


class BuscarLeadsMesResponse(BaseModel):
    leads_mes: int
    porcentagem_crescimento: float


class BuscarMembrosMesResponse(BaseModel):
    membros_mes: int
    porcentagem_crescimento: float


class BuscarDoacoesECampanhasDoMembroResponse(BaseModel):
    quantia_total_doada: float | None
    num_doacoes: int | None
    num_registros_em_campanhas: int | None
    data_ultima_doacao: datetime | str | None

    @field_validator('data_ultima_doacao')
    @classmethod
    def formatar_datetime(cls, value: datetime):
        if isinstance(value, (str, NoneType)):
            return value

        return value.strftime('%d/%m/%Y %H:%M')
