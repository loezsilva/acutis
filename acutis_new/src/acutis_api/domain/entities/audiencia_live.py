import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from acutis_api.domain.database import table_registry


@table_registry.mapped_as_dataclass
class AudienciaLive:
    __tablename__ = 'audiencia_lives'

    id: Mapped[uuid.UUID] = mapped_column(
        init=False, primary_key=True, default_factory=uuid.uuid4
    )
    fk_live_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('lives.id'), index=True
    )
    titulo: Mapped[str] = mapped_column(String(155), nullable=False)
    audiencia: Mapped[int] = mapped_column(Integer, nullable=False)
    data_hora_registro: Mapped[datetime] = mapped_column(
        DateTime, default=func.now()
    )
