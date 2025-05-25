import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from acutis_api.domain.database import table_registry


class VocationalSacramentsEnum(str, Enum):
    batismo = 'batismo'
    crisma = 'crisma'
    eucaristia = 'eucaristia'
    penitencia = 'penitencia'
    uncao_dos_enfermos = 'uncao_dos_enfermos'
    ordem = 'ordem'
    matrimonio = 'matrimonio'


@table_registry.mapped_as_dataclass
class SacramentoVocacional:
    __tablename__ = 'sacramentos_vocacional'

    id: Mapped[uuid.UUID] = mapped_column(
        init=False, primary_key=True, default_factory=uuid.uuid4, index=True
    )
    fk_ficha_vocacional_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('fichas_vocacional.id'),
        nullable=False,
        index=True,
    )
    nome: Mapped[VocationalSacramentsEnum] = mapped_column(nullable=False)
    criado_em: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    atualizado_em: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )
