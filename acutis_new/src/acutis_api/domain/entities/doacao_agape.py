import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from acutis_api.domain.database import table_registry
from acutis_api.domain.entities.modelo_base import ModeloBase


@table_registry.mapped_as_dataclass
class DoacaoAgape(ModeloBase):
    __tablename__ = 'doacoes_agape'

    fk_familia_agape_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('familias_agape.id'),
        index=True,
    )
