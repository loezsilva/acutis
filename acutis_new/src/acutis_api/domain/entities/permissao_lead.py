import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from acutis_api.domain.database import table_registry
from acutis_api.domain.entities.modelo_base import ModeloBase

if TYPE_CHECKING:
    from acutis_api.domain.entities import Lead, Perfil, Sistema


@table_registry.mapped_as_dataclass
class PermissaoLead(ModeloBase):
    __tablename__ = 'permissoes_lead'

    lead_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('leads.id'), nullable=False, index=True
    )
    criado_por_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey('leads.id'), nullable=True
    )

    perfil_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('perfis.id'),
        nullable=False,
        index=True,
    )

    sistema_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey('sistema.id'), nullable=True, default=None
    )

    alterado_por_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey('leads.id'),
        nullable=True,
        default=None,
    )

    criado_por: Mapped['Lead'] = relationship(
        init=False, foreign_keys=[criado_por_id], backref='permissoes_criadas'
    )

    alterado_por: Mapped['Lead'] = relationship(
        init=False,
        foreign_keys=[alterado_por_id],
        backref='permissoes_aprovadas',
    )

    lead: Mapped['Lead'] = relationship(
        init=False, back_populates='permissoes_lead', foreign_keys=[lead_id]
    )

    perfil: Mapped['Perfil'] = relationship(
        init=False,
        back_populates='permissoes_lead',
        foreign_keys=[perfil_id],
    )

    sistema: Mapped['Sistema'] = relationship(
        init=False,
        back_populates='permissoes_leads',
        foreign_keys=[sistema_id],
    )
