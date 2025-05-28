import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, func, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from acutis_api.domain.database import table_registry
from acutis_api.domain.entities.modelo_base import ModeloBase

if TYPE_CHECKING:
    from acutis_api.domain.entities.perfil import Perfil  # noqa
    from acutis_api.domain.entities.menu_sistema import MenuSistema  # noqa


@table_registry.mapped_as_dataclass
class PermissaoMenu(ModeloBase):
    __tablename__ = 'permissoes_menu'

    id: Mapped[uuid.UUID] = mapped_column(
        init=False, primary_key=True, default_factory=uuid.uuid4
    )
    perfil_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('perfis.id'), nullable=False, index=True
    )
    menu_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('menus_sistema.id'), nullable=False, index=True
    )
    acessar: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    criar: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    editar: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    deletar: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Relationships
    perfil: Mapped['Perfil'] = relationship(back_populates='permissoes_menu')
    menu: Mapped['MenuSistema'] = relationship(back_populates='permissoes_menu')

    criado_em: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    atualizado_em: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )
