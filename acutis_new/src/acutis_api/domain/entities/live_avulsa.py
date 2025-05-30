import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from acutis_api.domain.database import table_registry


@table_registry.mapped_as_dataclass
class LiveAvulsa:
    __tablename__ = 'lives_avulsas'

    id: Mapped[uuid.UUID] = mapped_column(
        init=False, primary_key=True, default_factory=uuid.uuid4
    )
    fk_live_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('lives.id'), index=True
    )
    data_hora_inicio: Mapped[datetime] = mapped_column(
        DateTime, nullable=False
    )
    criado_em: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    criado_por: Mapped[uuid.UUID] = mapped_column(ForeignKey('membros.id'))
    atualizado_em: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )
