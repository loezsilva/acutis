import uuid
from datetime import date, datetime

from pydantic import Field

from acutis_api.communication.enums import TipoOrdenacaoEnum
from acutis_api.communication.enums.admin_doacoes import (
    FormaPagamentoEnum,
    GatewayPagamentoEnum,
    ListarDoacoesOrdenarPorEnum,
    StatusProcessamentoEnum,
)
from acutis_api.communication.requests.paginacao import PaginacaoQuery


class ListarDoacoesQuery(PaginacaoQuery):
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
    ordenar_por: ListarDoacoesOrdenarPorEnum = (
        ListarDoacoesOrdenarPorEnum.doacao_criada_em
    )
    tipo_ordenacao: TipoOrdenacaoEnum = TipoOrdenacaoEnum.decrescente
