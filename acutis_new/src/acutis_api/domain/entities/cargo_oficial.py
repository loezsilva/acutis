import uuid
from datetime import datetime

from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column

from acutis_api.domain.database import table_registry


@table_registry.mapped_as_dataclass
class CargosOficiais:
    __tablename__ = 'cargos_oficiais'

    id: Mapped[uuid.UUID] = mapped_column(
        index=True, init=False, primary_key=True, default_factory=uuid.uuid4
    )
    nome_cargo: Mapped[str] = mapped_column(
        String(50), nullable=False, unique=True, index=True
    )
    fk_cargo_superior_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey('cargos_oficiais.id'), nullable=True
    )
    criado_por: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('membros.id'),
        nullable=False,  # nosonar
    )
    criado_em: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )
    atualizado_por: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey('membros.id')  # nosonar
    )
    atualizado_em: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )
