import uuid
from datetime import datetime

from pydantic import BaseModel

from acutis_api.domain.entities.pagamento_doacao import (
    FormaPagamentoEnum,
    GatewayPagamentoEnum,
)
from acutis_api.domain.entities.processamento_doacao import (
    StatusProcessamentoEnum,
)


class RegistrarDoacaoSchema(BaseModel):
    benfeitor_id: uuid.UUID
    campanha_doacao_id: uuid.UUID
    valor_doacao: float
    recorrente: bool
    forma_pagamento: FormaPagamentoEnum
    codigo_ordem_pagamento: str | None = None
    anonimo: bool
    gateway: GatewayPagamentoEnum
    codigo_referencia: str | None = None
    codigo_transacao: str
    nosso_numero: str | None = None
    processado_em: datetime | None = None
    status: StatusProcessamentoEnum
