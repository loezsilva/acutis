import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from acutis_api.domain.database import table_registry

if TYPE_CHECKING:
    from acutis_api.domain.entities import Coordenada  # pragma: no cover


@table_registry.mapped_as_dataclass
class Endereco:
    __tablename__ = 'enderecos'

    id: Mapped[uuid.UUID] = mapped_column(
        init=False, primary_key=True, default_factory=uuid.uuid4
    )
    codigo_postal: Mapped[str | None]
    tipo_logradouro: Mapped[str | None]
    logradouro: Mapped[str | None]
    numero: Mapped[str | None]
    complemento: Mapped[str | None]
    bairro: Mapped[str | None]
    cidade: Mapped[str | None]
    estado: Mapped[str | None]
    pais: Mapped[str | None]
    obriga_atualizar_endereco: Mapped[bool | None] = mapped_column(
        index=True, default=True
    )
    criado_em: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    atualizado_em: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )

    coordenada: Mapped['Coordenada'] = relationship(
        init=False, backref='endereco'
    )
