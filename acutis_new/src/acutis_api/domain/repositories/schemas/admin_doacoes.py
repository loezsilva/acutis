import uuid
from datetime import date, datetime

from pydantic import BaseModel

from acutis_api.domain.entities.pagamento_doacao import (
    FormaPagamentoEnum,
    GatewayPagamentoEnum,
)
from acutis_api.domain.entities.processamento_doacao import (
    StatusProcessamentoEnum,
)
from acutis_api.domain.repositories.enums import TipoOrdenacaoEnum
from acutis_api.domain.repositories.schemas.paginacao import PaginacaoQuery


class ListarDoacoesQuery(PaginacaoQuery):
    nome_email_documento: str = ''
    campanha_id: uuid.UUID | None = None
    campanha_nome: str = ''
    data_doacao_criada_em_inicial: date | None = None
    data_doacao_criada_em_final: date = datetime.now().date()
    data_doacao_cancelada_em_inicial: date | None = None
    data_doacao_cancelada_em_final: date = datetime.now().date()
    recorrente: bool | None = None
    forma_pagamento: FormaPagamentoEnum | None = None
    codigo_ordem_pagamento: str = ''
    anonimo: bool | None = None
    gateway: GatewayPagamentoEnum | None = None
    ativo: bool | None = None
    doacao_processada_em_inicial: date | None = None
    doacao_processada_em_final: date = datetime.now().date()
    codigo_transacao: str = ''
    codigo_comprovante: str = ''
    nosso_numero: str = ''
    status: StatusProcessamentoEnum | None = None
    ordenar_por: str = 'doacao_criada_em'
    tipo_ordenacao: TipoOrdenacaoEnum = TipoOrdenacaoEnum.decrescente


class ListarDoacoesSchema(BaseModel):
    benfeitor_id: uuid.UUID
    benfeitor_nome: str
    lead_id: uuid.UUID | None
    membro_id: uuid.UUID | None
    campanha_id: uuid.UUID
    campanha_nome: str
    doacao_id: uuid.UUID
    doacao_criada_em: datetime
    doacao_cancelada_em: datetime | None
    pagamento_doacao_id: uuid.UUID
    valor_doacao: float
    recorrente: bool
    forma_pagamento: FormaPagamentoEnum
    codigo_ordem_pagamento: str | None
    anonimo: bool
    gateway: GatewayPagamentoEnum
    ativo: bool
    processamento_doacao_id: uuid.UUID
    processado_em: datetime | None
    codigo_referencia: str | None
    codigo_transacao: str | None
    codigo_comprovante: str | None
    nosso_numero: str | None
    status: StatusProcessamentoEnum
