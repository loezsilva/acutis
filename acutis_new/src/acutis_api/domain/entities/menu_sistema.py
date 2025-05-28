import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from acutis_api.domain.database import table_registry
from acutis_api.domain.entities.modelo_base import ModeloBase

if TYPE_CHECKING:
    from acutis_api.domain.entities import (
        PermissaoMenu
    )


@table_registry.mapped_as_dataclass
class MenuSistema(ModeloBase):
    __tablename__ = 'menus_sistema'

    id: Mapped[uuid.UUID] = mapped_column(
        init=False, primary_key=True, default_factory=uuid.uuid4
    )
    nome: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    descricao: Mapped[str | None] = mapped_column(String(255))

    # Relationships
    permissoes_menu: Mapped[list['PermissaoMenu']] = relationship(
        back_populates='menu', cascade='all, delete-orphan'
    )

    criado_em: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    atualizado_em: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )
