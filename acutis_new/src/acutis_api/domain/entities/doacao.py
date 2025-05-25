import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from acutis_api.domain.database import table_registry

if TYPE_CHECKING:
    from acutis_api.domain.entities import PagamentoDoacao


@table_registry.mapped_as_dataclass
class Doacao:
    __tablename__ = 'doacoes'

    id: Mapped[uuid.UUID] = mapped_column(
        init=False, primary_key=True, default_factory=uuid.uuid4
    )
    fk_benfeitor_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('benfeitores.id'), index=True
    )
    fk_campanha_doacao_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('campanhas_doacoes.id'), index=True
    )
    cancelado_em: Mapped[datetime | None] = mapped_column(default=None)
    cancelado_por: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey('membros.id'), default=None
    )
    contabilizar: Mapped[bool] = mapped_column(index=True, default=True)
    criado_em: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    atualizado_em: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )

    pagamento_doacao: Mapped['PagamentoDoacao'] = relationship(
        init=False, back_populates='doacao'
    )
