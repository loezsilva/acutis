import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from acutis_api.domain.database import table_registry
from acutis_api.domain.entities.modelo_base import ModeloBase

if TYPE_CHECKING:
    from acutis_api.domain.entities import MenuSistema, Perfil


@table_registry.mapped_as_dataclass
class PermissaoMenu(ModeloBase):
    __tablename__ = 'permissoes_menu'

    perfil_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('perfis.id'), nullable=False, index=True
    )
    menu_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('menus_sistema.id'), nullable=False, index=True
    )

    perfil: Mapped['Perfil'] = relationship(
        init=False,
        foreign_keys=[perfil_id],
        back_populates='permissoes_menu',
    )
    menu: Mapped['MenuSistema'] = relationship(
        init=False, foreign_keys=[menu_id], back_populates='permissoes_menu'
    )

    # Campos com valor padrão
    acessar: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    criar: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    editar: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    deletar: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
