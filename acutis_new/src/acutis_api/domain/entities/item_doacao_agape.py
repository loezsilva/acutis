import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from acutis_api.domain.database import table_registry
from acutis_api.domain.entities.modelo_base import ModeloBase


@table_registry.mapped_as_dataclass
class ItemDoacaoAgape(ModeloBase):
    __tablename__ = 'itens_doacoes_agape'

    fk_item_instancia_agape_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('itens_instancias_agape.id'), index=True
    )
    fk_doacao_agape_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('doacoes_agape.id'), index=True
    )
    quantidade: Mapped[int]
