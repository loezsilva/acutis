import uuid
from datetime import datetime

from sqlalchemy import ForeignKey, UnicodeText, func
from sqlalchemy.orm import Mapped, mapped_column

from acutis_api.domain.database import table_registry


@table_registry.mapped_as_dataclass
class LandingPage:
    __tablename__ = 'landing_pages'

    id: Mapped[uuid.UUID] = mapped_column(
        init=False, primary_key=True, default_factory=uuid.uuid4
    )
    fk_campanha_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('campanhas.id'), index=True
    )
    conteudo: Mapped[str] = mapped_column(UnicodeText)
    shlink: Mapped[str | None]
    criado_em: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    atualizado_em: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )
