import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from acutis_api.domain.database import table_registry
from acutis_api.domain.entities.modelo_base import ModeloBase

if TYPE_CHECKING:
    from acutis_api.domain.entities import (
        Lead,
        Perfil
    )


@table_registry.mapped_as_dataclass
class PermissaoLead(ModeloBase):
    __tablename__ = 'permissoes_lead'

    id: Mapped[uuid.UUID] = mapped_column(
        init=False, primary_key=True, default_factory=uuid.uuid4
    )
    lead_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('leads.id'), nullable=False, index=True
    )
    perfil_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('perfis.id'), nullable=False, index=True
    )

    # Relationships
    lead: Mapped['Lead'] = relationship(back_populates='permissoes_lead')
    perfil: Mapped['Perfil'] = relationship(back_populates='permissoes_lead')

    criado_em: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    atualizado_em: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )
