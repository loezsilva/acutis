import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UnicodeText, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from acutis_api.domain.database import table_registry

if TYPE_CHECKING:  # pragma: no cover
    from acutis_api.domain.entities.campo_adicional import CampoAdicional


@table_registry.mapped_as_dataclass
class MetadadoLead:
    __tablename__ = 'metadados_leads'

    id: Mapped[uuid.UUID] = mapped_column(
        init=False, primary_key=True, default_factory=uuid.uuid4
    )
    fk_lead_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('leads.id'), index=True
    )
    fk_campo_adicional_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('campos_adicionais.id'), index=True
    )
    valor_campo: Mapped[str] = mapped_column(UnicodeText)
    criado_em: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    atualizado_em: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )

    campo_adicional: Mapped['CampoAdicional'] = relationship(
        init=False, backref='metadado_lead'
    )
