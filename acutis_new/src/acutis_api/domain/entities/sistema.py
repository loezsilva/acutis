import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from acutis_api.domain.database import table_registry
from acutis_api.domain.entities.modelo_base import ModeloBase

if TYPE_CHECKING:
    from acutis_api.domain.entities import (
        Lead,
        Perfil,
        PermissaoLead,
    )


@table_registry.mapped_as_dataclass
class Sistema(ModeloBase):
    __tablename__ = 'sistema'

    nome: Mapped[str] = mapped_column(String(20), nullable=False)
    descricao: Mapped[str] = mapped_column(String(200), nullable=False)
    versao: Mapped[str] = mapped_column(String(15), nullable=False)
    criado_por_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('leads.id'),
        init=False,
        nullable=True,
    )
    alterado_por_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey('leads.id'),
        nullable=True,
    )
    criado_por: Mapped['Lead'] = relationship(
        init=False,
        foreign_keys=[criado_por_id],
    )
    alterado_por: Mapped['Lead'] = relationship(
        init=False,
        foreign_keys=[alterado_por_id],
    )
    perfis: Mapped[list['Perfil']] = relationship(
        backref='system', lazy='dynamic'
    )
    permissoes_leads: Mapped[list['PermissaoLead']] = relationship(
        lazy='dynamic', back_populates='sistema'
    )
