import uuid
from datetime import datetime
from types import NoneType

from pydantic import BaseModel, ConfigDict, field_validator

from acutis_api.communication.responses.padrao import PaginacaoResponse


class RegistrarNovoMembroResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    nome: str


class RegistrarNovoLeadResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    nome: str


class DoacaoMembroBenfeitorSchema(BaseModel):
    nome_campanha: str
    foto_campanha: str | None
    tipo_doacao: str
    doacao_id: uuid.UUID


class DoacoesMembroBenfeitorResponse(PaginacaoResponse):
    doacoes: list[DoacaoMembroBenfeitorSchema]


class HistoricoDoacaoSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    data_doacao: datetime | str
    forma_pagamento: str
    status_processamento: str
    valor_doacao: float

    @field_validator('data_doacao')
    @classmethod
    def formatar_data(cls, value: datetime):
        if isinstance(value, (str, NoneType)):
            return value

        return value.strftime('%d/%m/%Y')


class HistoricoDoacaoResponse(PaginacaoResponse):
    historico_doacao: list[HistoricoDoacaoSchema]


class TotalPagoDoacoesSchema(BaseModel):
    valor_doado: float
    quantidade_doacoes: int


class UltimaDoacaoPagaSchema(BaseModel):
    ultima_doacao: datetime | str | None

    @field_validator('ultima_doacao')
    @classmethod
    def formatar_data(cls, value: datetime):
        if isinstance(value, (str, NoneType)):
            return value

        return value.strftime('%d/%m/%Y')


class CardDoacoesMembroBenfeitorResponse(BaseModel):
    total_pago_doacoes: TotalPagoDoacoesSchema
    ultima_doacao_paga: UltimaDoacaoPagaSchema
