import uuid
from datetime import datetime
from types import NoneType

from pydantic import BaseModel, ConfigDict, field_validator

from acutis_api.communication.responses.padrao import PaginacaoResponse


class CardsBenfeitoresTotalPercentualSchema(BaseModel):
    total: int | float
    percentual: float


class BuscarCardsBenfeitoresResponse(BaseModel):
    benfeitores: CardsBenfeitoresTotalPercentualSchema
    doacoes_anonimas: CardsBenfeitoresTotalPercentualSchema
    montante: CardsBenfeitoresTotalPercentualSchema
    ticket_medio: CardsBenfeitoresTotalPercentualSchema


class ListarBenfeitoresSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    nome: str
    numero_documento: str
    registrado_em: datetime | str | None
    quantidade_doacoes: int
    montante_total: float
    ultima_doacao: datetime | str | None

    @field_validator('registrado_em', 'ultima_doacao')
    @classmethod
    def formatar_datetime(cls, value: datetime):
        if isinstance(value, (str, NoneType)):
            return value

        return value.strftime('%d/%m/%Y - %H:%M')

    @field_validator('montante_total')
    @classmethod
    def formatar_montante_total(cls, value: float):
        return round(value, 2)


class ListarBenfeitoresResponse(PaginacaoResponse):
    benfeitores: list[ListarBenfeitoresSchema]


class BuscarInformacoesBenfeitorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    nome: str
    numero_documento: str
    registrado_em: datetime | str | None
    total_doacoes: int
    total_valor_doado: float
    ultima_doacao: datetime | str | None

    @field_validator('registrado_em', 'ultima_doacao')
    @classmethod
    def formatar_datetime(cls, value: datetime):
        if isinstance(value, (str, NoneType)):
            return value

        return value.strftime('%d/%m/%Y')

    @field_validator('total_valor_doado')
    @classmethod
    def formatar_montante_total(cls, value: float):
        return round(value, 2)


class ListarDoacoesAnonimasBenfeitorSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    data: datetime | str | None
    hora: datetime | str | None
    valor: float

    @field_validator('data')
    @classmethod
    def formatar_data(cls, value: datetime):
        if isinstance(value, (str, NoneType)):
            return value

        return value.strftime('%d/%m/%Y')

    @field_validator('hora')
    @classmethod
    def formatar_hora(cls, value: datetime):
        if isinstance(value, (str, NoneType)):
            return value

        return value.strftime('%H:%M:%S')


class ListarDoacoesAnonimasBenfeitorResponse(PaginacaoResponse):
    doacoes: list[ListarDoacoesAnonimasBenfeitorSchema]
