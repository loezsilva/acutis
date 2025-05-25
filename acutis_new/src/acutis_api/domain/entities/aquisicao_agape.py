import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from acutis_api.domain.database import table_registry
from acutis_api.domain.entities.modelo_base import ModeloBase


@table_registry.mapped_as_dataclass
class AquisicaoAgape(ModeloBase):
    __tablename__ = 'aquisicoes_agape'

    fk_estoque_agape_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('estoques_agape.id'),
        index=True,
    )
    quantidade: Mapped[int]
