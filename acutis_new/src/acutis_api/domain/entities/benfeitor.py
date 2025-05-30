import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Index, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from acutis_api.domain.database import table_registry

if TYPE_CHECKING:
    from acutis_api.domain.entities import Membro


@table_registry.mapped_as_dataclass
class Benfeitor:
    __tablename__ = 'benfeitores'

    id: Mapped[uuid.UUID] = mapped_column(
        init=False, primary_key=True, default_factory=uuid.uuid4
    )
    numero_documento: Mapped[str | None] = mapped_column(String(50))
    nome: Mapped[str]
    contabilizar: Mapped[bool] = mapped_column(index=True, default=True)
    criado_em: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    atualizado_em: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )

    membro: Mapped['Membro'] = relationship(
        init=False, back_populates='benfeitor'
    )


ix_benfeitores_numero_documento = Index(
    'ix_benfeitores_numero_documento',
    Benfeitor.numero_documento,
    unique=True,
    mssql_where=Benfeitor.numero_documento.isnot(None),
)
