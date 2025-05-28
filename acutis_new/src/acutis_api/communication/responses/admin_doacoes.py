import uuid
from datetime import datetime
from types import NoneType

from pydantic import BaseModel, field_validator

from acutis_api.communication.enums.admin_doacoes import (
    FormaPagamentoEnum,
    GatewayPagamentoEnum,
    StatusProcessamentoEnum,
)
from acutis_api.communication.responses.padrao import PaginacaoResponse


class DadosBenfeitorSchema(BaseModel):
    id: uuid.UUID
    nome: str
    lead_id: uuid.UUID | None
    membro_id: uuid.UUID | None


class DadosCampanhaSchema(BaseModel):
    id: uuid.UUID
    nome: str


class DadosDoacaoSchema(BaseModel):
    id: uuid.UUID
    criada_em: datetime | str | None
    cancelada_em: datetime | str | None
    pagamento_doacao_id: uuid.UUID
    valor_doacao: float
    recorrente: bool
    forma_pagamento: FormaPagamentoEnum
    codigo_ordem_pagamento: str | None
    anonimo: bool
    gateway: GatewayPagamentoEnum
    ativo: bool
    processamento_doacao_id: uuid.UUID
    processado_em: datetime | str | None
    codigo_referencia: str | None
    codigo_transacao: str | None
    codigo_comprovante: str | None
    nosso_numero: str | None
    status: StatusProcessamentoEnum

    @field_validator('criada_em', 'cancelada_em', 'processado_em')
    @classmethod
    def formatar_datetime(cls, value: datetime):
        if isinstance(value, (str, NoneType)):
            return value

        return value.strftime('%d/%m/%Y %H:%M')


class ListarDoacoesSchema(BaseModel):
    benfeitor: DadosBenfeitorSchema
    campanha: DadosCampanhaSchema
    doacao: DadosDoacaoSchema


class ListarDoacoesResponse(PaginacaoResponse):
    doacoes: list[ListarDoacoesSchema]
