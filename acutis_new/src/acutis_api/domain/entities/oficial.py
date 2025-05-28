import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from acutis_api.domain.database import table_registry


class CargosEnum(str, Enum):
    general = 'general'
    marechal = 'marechal'


class StatusOficialEnum(str, Enum):
    aprovado = 'aprovado'
    pendente = 'pendente'
    recusado = 'recusado'


@table_registry.mapped_as_dataclass
class Oficial:
    __tablename__ = 'oficiais'

    id: Mapped[uuid.UUID] = mapped_column(
        init=False, primary_key=True, default_factory=uuid.uuid4
    )
    fk_membro_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('membros.id'),  # NOSONAR
        index=True,
        unique=True,
    )
    fk_superior_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey('membros.id'),  # NOSONAR
        index=True,
    )
    fk_cargo_oficial_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('cargos_oficiais.id'), index=True, nullable=True
    )
    status: Mapped[StatusOficialEnum] = mapped_column(index=True)
    criado_em: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    atualizado_em: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )

    atualizado_por: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey('membros.id'),
        nullable=True,  # nosonar
    )
