import uuid
from datetime import datetime, time

from sqlalchemy import ForeignKey, String, Time, func
from sqlalchemy.orm import Mapped, mapped_column

from acutis_api.domain.database import table_registry


@table_registry.mapped_as_dataclass
class LiveRecorrente:
    __tablename__ = 'lives_recorrentes'

    id: Mapped[uuid.UUID] = mapped_column(
        init=False, primary_key=True, default_factory=uuid.uuid4
    )
    dia_semana: Mapped[str] = mapped_column(String(50), nullable=False)
    hora_inicio: Mapped[time] = mapped_column(Time, nullable=False)
    fk_live_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('lives.id'), index=True
    )
    criado_em: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    criado_por: Mapped[uuid.UUID] = mapped_column(ForeignKey('membros.id'))
    atualizado_em: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )
