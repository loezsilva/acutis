import uuid
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from acutis_api.domain.database import table_registry
from acutis_api.domain.entities.pagamento_doacao import FormaPagamentoEnum

if TYPE_CHECKING:  # pragma: no cover
    from acutis_api.domain.entities import PagamentoDoacao


class StatusProcessamentoEnum(str, Enum):
    pendente = 'pendente'
    pago = 'pago'
    expirado = 'expirado'
    estornado = 'estornado'


@table_registry.mapped_as_dataclass
class ProcessamentoDoacao:
    __tablename__ = 'processamentos_doacoes'

    id: Mapped[uuid.UUID] = mapped_column(
        init=False, primary_key=True, default_factory=uuid.uuid4
    )
    fk_pagamento_doacao_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('pagamentos_doacoes.id'), index=True
    )
    forma_pagamento: Mapped[FormaPagamentoEnum] = mapped_column(index=True)
    processado_em: Mapped[datetime | None] = mapped_column(default=None)
    codigo_referencia: Mapped[str | None] = mapped_column(default=None)
    codigo_transacao: Mapped[str | None] = mapped_column(default=None)
    codigo_comprovante: Mapped[str | None] = mapped_column(default=None)
    nosso_numero: Mapped[str | None] = mapped_column(default=None)
    status: Mapped[StatusProcessamentoEnum] = mapped_column(
        index=True, default=StatusProcessamentoEnum.pendente
    )
    criado_em: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    atualizado_em: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )

    pagamento_doacao: Mapped['PagamentoDoacao'] = relationship(
        init=False, back_populates='processamentos_doacoes'
    )
