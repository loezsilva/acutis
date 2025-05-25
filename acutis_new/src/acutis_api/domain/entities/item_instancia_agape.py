import uuid
from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from acutis_api.domain.database import table_registry


@table_registry.mapped_as_dataclass
class ItemInstanciaAgape:
    __tablename__ = 'itens_instancias_agape'

    id: Mapped[uuid.UUID] = mapped_column(
        init=False, primary_key=True, default_factory=uuid.uuid4
    )
    fk_estoque_agape_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('estoques_agape.id'), index=True
    )
    fk_instancia_acao_agape_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('instancias_acoes_agape.id'), index=True
    )
    quantidade: Mapped[int]
    criado_em: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    atualizado_em: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )
