import uuid
from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from acutis_api.domain.database import table_registry


@table_registry.mapped_as_dataclass
class Coordenada:
    __tablename__ = 'coordenadas'

    id: Mapped[uuid.UUID] = mapped_column(
        init=False, primary_key=True, default_factory=uuid.uuid4
    )
    fk_endereco_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('enderecos.id'), index=True
    )
    latitude: Mapped[float]
    longitude: Mapped[float]
    latitude_ne: Mapped[float]
    longitude_ne: Mapped[float]
    latitude_so: Mapped[float]
    longitude_so: Mapped[float]
    criado_em: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    atualizado_em: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )
