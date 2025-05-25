import uuid
from datetime import datetime

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from acutis_api.domain.database import table_registry
from acutis_api.domain.entities.modelo_base import ModeloBase


@table_registry.mapped_as_dataclass
class FamiliaAgape(ModeloBase):
    __tablename__ = 'familias_agape'

    fk_endereco_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('enderecos.id'),
        index=True,
    )
    nome_familia: Mapped[str] = mapped_column(String(100), index=True)
    status: Mapped[bool] = mapped_column(index=True)
    observacao: Mapped[str | None]
    comprovante_residencia: Mapped[str | None]
    deletado_em: Mapped[datetime | None]
    cadastrada_por: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('membros.id'), nullable=False, index=True
    )
    membros = relationship(
        'MembroAgape', backref='familia', cascade='all, delete'
    )
