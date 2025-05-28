import uuid
from datetime import date, datetime
from typing import Any

from pydantic import BaseModel, EmailStr, SecretStr

from acutis_api.domain.entities.lead import OrigemCadastroEnum
from acutis_api.domain.entities.membro import SexoEnum


class RegistrarNovoMembroSchema(BaseModel):
    nome_social: str
    data_nascimento: date | None = None
    numero_documento: str | None = None
    sexo: SexoEnum | None = None
    foto: str | None = None
    endereco_id: uuid.UUID
    lead_id: uuid.UUID
    benfeitor_id: uuid.UUID | None = None


class RegistrarNovoLeadSchema(BaseModel):
    nome: str
    email: EmailStr
    telefone: str
    pais: str
    origem_cadastro: OrigemCadastroEnum
    senha: SecretStr
    status: bool


class RegistrarNovoEnderecoSchema(BaseModel):
    codigo_postal: str | None = None
    tipo_logradouro: str | None = None
    logradouro: str | None = None
    numero: str | None = None
    complemento: str | None = None
    bairro: str | None = None
    cidade: str | None = None
    estado: str | None = None
    pais: str | None = None


class CampoAdicionalSchema(BaseModel):
    campo_adicional_id: uuid.UUID
    valor_campo: Any


class DoacaoMembroBenfeitorSchema(BaseModel):
    nome_campanha: str
    foto_campanha: str | None
    tipo_doacao: str
    doacao_id: uuid.UUID


class HistoricoDoacaoSchema(BaseModel):
    data_doacao: datetime
    forma_pagamento: str
    status_processamento: str
    valor_doacao: float


class CardDoacoesMembroBenfeitorSchema(BaseModel):
    ultima_doacao: datetime | None
    quantidade_doacoes: int
    valor_doado: float
