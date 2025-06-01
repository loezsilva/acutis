from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from acutis_api.domain.database import table_registry
from acutis_api.domain.entities.modelo_base import ModeloBase


@table_registry.mapped_as_dataclass
class EstoqueAgape(ModeloBase):
    __tablename__ = 'estoques_agape'

    item: Mapped[str] = mapped_column(String(100), index=True)
    quantidade: Mapped[int]
