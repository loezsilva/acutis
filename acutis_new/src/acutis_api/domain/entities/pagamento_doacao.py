import uuid
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from acutis_api.domain.database import table_registry

if TYPE_CHECKING:  # pragma: no cover
    from acutis_api.domain.entities import Doacao, ProcessamentoDoacao


class FormaPagamentoEnum(str, Enum):
    pix = 'pix'
    credito = 'credito'
    boleto = 'boleto'


class GatewayPagamentoEnum(str, Enum):
    maxipago = 'maxipago'
    mercado_pago = 'mercado_pago'
    itau = 'itau'


@table_registry.mapped_as_dataclass
class PagamentoDoacao:
    __tablename__ = 'pagamentos_doacoes'

    id: Mapped[uuid.UUID] = mapped_column(
        init=False, primary_key=True, default_factory=uuid.uuid4
    )
    fk_doacao_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('doacoes.id'), index=True
    )
    valor: Mapped[float]
    recorrente: Mapped[bool] = mapped_column(index=True)
    forma_pagamento: Mapped[FormaPagamentoEnum] = mapped_column(index=True)
    codigo_ordem_pagamento: Mapped[str | None] = mapped_column(
        String(100), index=True
    )
    anonimo: Mapped[bool] = mapped_column(index=True)
    gateway: Mapped[GatewayPagamentoEnum] = mapped_column(index=True)
    ativo: Mapped[bool] = mapped_column(index=True, default=True)
    criado_em: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    atualizado_em: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )

    doacao: Mapped['Doacao'] = relationship(
        init=False, back_populates='pagamento_doacao'
    )
    processamentos_doacoes: Mapped[list['ProcessamentoDoacao']] = relationship(
        init=False, back_populates='pagamento_doacao'
    )
