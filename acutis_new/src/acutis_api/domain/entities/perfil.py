import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, func, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from acutis_api.domain.database import table_registry
from acutis_api.domain.entities.modelo_base import ModeloBase

if TYPE_CHECKING:
    from acutis_api.domain.entities.permissao_lead import PermissaoLead
    from acutis_api.domain.entities.permissao_menu import PermissaoMenu


@table_registry.mapped_as_dataclass
class Perfil(ModeloBase):
    __tablename__ = 'perfis'

    id: Mapped[uuid.UUID] = mapped_column(
        init=False, primary_key=True, default_factory=uuid.uuid4
    )
    
    permissoes_lead: Mapped[list['PermissaoLead']] = relationship(
        back_populates='perfil', cascade='all, delete-orphan'
    )
    permissoes_menu: Mapped[list['PermissaoMenu']] = relationship(
        back_populates='perfil', cascade='all, delete-orphan'
    )

    nome: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    status: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    super_perfil: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    
    # Relationships

    criado_em: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    atualizado_em: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )
