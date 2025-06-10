import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from acutis_api.domain.database import table_registry
from acutis_api.domain.entities.modelo_base import ModeloBase

if TYPE_CHECKING:
    from acutis_api.domain.entities import Lead, PermissaoLead, PermissaoMenu


@table_registry.mapped_as_dataclass
class Perfil(ModeloBase):
    __tablename__ = 'perfis'

    sistema_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey('sistema.id'),
        init=False,
        nullable=True,
    )

    criado_por_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey('leads.id'), nullable=True
    )

    alterado_por_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey('leads.id'), init=False, nullable=True
    )

    permissoes_lead: Mapped[list['PermissaoLead']] = relationship(
        back_populates='perfil', cascade='all, delete-orphan'
    )
    permissoes_menu: Mapped[list['PermissaoMenu']] = relationship(
        back_populates='perfil', cascade='all, delete-orphan'
    )

    criado_por: Mapped['Lead'] = relationship(
        init=False,
        foreign_keys=[criado_por_id],
    )

    alterado_por: Mapped['Lead'] = relationship(
        init=False,
        foreign_keys=[alterado_por_id],
    )

    nome: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    status: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    super_perfil: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
