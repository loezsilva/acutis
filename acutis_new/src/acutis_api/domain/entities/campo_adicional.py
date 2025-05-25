import uuid
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from acutis_api.domain.database import table_registry

if TYPE_CHECKING:  # pragma: no cover
    from acutis_api.domain.entities.campanha import Campanha


class TiposCampoEnum(str, Enum):
    string = 'string'
    integer = 'int'
    float = 'float'
    date = 'date'
    datetime = 'datetime'
    arquivo = 'arquivo'


@table_registry.mapped_as_dataclass
class CampoAdicional:
    __tablename__ = 'campos_adicionais'

    id: Mapped[uuid.UUID] = mapped_column(
        init=False, primary_key=True, default_factory=uuid.uuid4
    )
    fk_campanha_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('campanhas.id'), index=True
    )
    nome_campo: Mapped[str]
    tipo_campo: Mapped[TiposCampoEnum]
    obrigatorio: Mapped[bool]
    criado_em: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    atualizado_em: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )

    campanha: Mapped['Campanha'] = relationship(
        init=False, back_populates='campos_adicionais'
    )
