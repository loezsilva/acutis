import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from acutis_api.domain.database import table_registry
from acutis_api.domain.entities.modelo_base import ModeloBase

if TYPE_CHECKING:
    from acutis_api.domain.entities import PermissaoMenu


@table_registry.mapped_as_dataclass
class MenuSistema(ModeloBase):
    __tablename__ = 'menus_sistema'

    nome: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    slug: str = mapped_column(String(50), nullable=False, unique=True)
    sistema_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey('sistema.id'),
        init=False,
        nullable=True,
    )
    criado_por_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('leads.id'),
        nullable=True,
    )
    alterado_por_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey('leads.id'),
        init=False,
        nullable=True,
    )

    # Relationships
    permissoes_menu: Mapped[list['PermissaoMenu']] = relationship(
        init=False, back_populates='menu', cascade='all, delete-orphan'
    )
