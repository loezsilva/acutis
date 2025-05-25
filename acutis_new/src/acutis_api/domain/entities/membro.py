import uuid
from datetime import date, datetime
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Index, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from acutis_api.domain.database import table_registry

if TYPE_CHECKING:
    from acutis_api.domain.entities import (  # pragma: no cover
        Benfeitor,
        Endereco,
        Lead,
    )


class SexoEnum(str, Enum):
    masculino = 'masculino'
    feminino = 'feminino'


@table_registry.mapped_as_dataclass
class Membro:
    __tablename__ = 'membros'

    id: Mapped[uuid.UUID] = mapped_column(
        init=False, primary_key=True, default_factory=uuid.uuid4
    )
    fk_lead_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('leads.id'), index=True, unique=True
    )
    fk_benfeitor_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey('benfeitores.id')
    )
    fk_endereco_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('enderecos.id'), index=True, unique=True
    )
    nome_social: Mapped[str | None]
    data_nascimento: Mapped[date | None]
    numero_documento: Mapped[str | None] = mapped_column(String(50))
    sexo: Mapped[SexoEnum | None]
    foto: Mapped[str | None]
    criado_em: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    atualizado_em: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )

    cadastro_atualizado_em: Mapped[datetime | None] = mapped_column(init=False)

    lead: Mapped['Lead'] = relationship(init=False, back_populates='membro')
    benfeitor: Mapped['Benfeitor'] = relationship(
        init=False, back_populates='membro'
    )
    endereco: Mapped['Endereco'] = relationship(init=False, backref='membro')


ix_membros_fk_benfeitor_id = Index(
    'ix_membros_fk_benfeitor_id',
    Membro.fk_benfeitor_id,
    unique=True,
    mssql_where=Membro.fk_benfeitor_id.isnot(None),
)

ix_membros_numero_documento = Index(
    'ix_membros_numero_documento',
    Membro.numero_documento,
    unique=True,
    mssql_where=Membro.numero_documento.isnot(None),
)
