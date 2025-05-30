import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from acutis_api.domain.database import table_registry

if TYPE_CHECKING:
    from acutis_api.domain.entities import Campanha, Membro


@table_registry.mapped_as_dataclass
class Live:
    __tablename__ = 'lives'

    id: Mapped[uuid.UUID] = mapped_column(
        init=False, primary_key=True, default_factory=uuid.uuid4
    )
    tag: Mapped[str] = mapped_column(String(100), nullable=False)
    fk_campanha_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('campanhas.id')
    )
    campanha: Mapped['Campanha'] = relationship(init=False, backref='lives')
    rede_social: Mapped[str] = mapped_column(String(50), nullable=False)
    criado_em: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    criado_por: Mapped[uuid.UUID] = mapped_column(ForeignKey('membros.id'))
    criador: Mapped['Membro'] = relationship(
        init=False, backref='lives_criadas'
    )
    atualizado_em: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )
