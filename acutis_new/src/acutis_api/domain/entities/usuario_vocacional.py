import uuid
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from acutis_api.domain.database import table_registry

if TYPE_CHECKING:
    from acutis_api.domain.entities import (  # pragma: no cover
        CadastroVocacional,
        EtapaVocacional,
        FichaVocacional,
    )


class GeneroVocacionalEnum(str, Enum):
    masculino = 'masculino'
    feminino = 'feminino'


@table_registry.mapped_as_dataclass
class UsuarioVocacional:
    __tablename__ = 'usuarios_vocacional'

    id: Mapped[uuid.UUID] = mapped_column(
        init=False, primary_key=True, default_factory=uuid.uuid4, index=True
    )
    nome: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(
        String(120), nullable=False, unique=True, index=True
    )
    telefone: Mapped[str] = mapped_column(nullable=False)
    genero: Mapped[GeneroVocacionalEnum] = mapped_column(nullable=False)
    pais: str = mapped_column(nullable=False)
    criado_em: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    atualizado_em: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )

    etapas: Mapped['EtapaVocacional'] = relationship(
        init=False, backref='usuario_vocacional', cascade='all, delete'
    )
    fichas: Mapped['FichaVocacional'] = relationship(
        init=False, backref='usuario_vocacional', cascade='all, delete'
    )
    cadastros: Mapped['CadastroVocacional'] = relationship(
        init=False, backref='usuario_vocacional', cascade='all, delete'
    )
