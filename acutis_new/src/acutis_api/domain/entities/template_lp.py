import uuid
from datetime import datetime

from sqlalchemy import ForeignKey, UnicodeText, func
from sqlalchemy.orm import Mapped, mapped_column

from acutis_api.domain.database import table_registry


@table_registry.mapped_as_dataclass
class TemplateLP:
    __tablename__ = 'templates_lp'

    id: Mapped[uuid.UUID] = mapped_column(
        init=False, primary_key=True, default_factory=uuid.uuid4
    )
    titulo: Mapped[str]
    conteudo: Mapped[str] = mapped_column(UnicodeText)
    criado_em: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    criado_por: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey('membros.id'),
        nullable=True,
    )
    atualizado_em: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )
