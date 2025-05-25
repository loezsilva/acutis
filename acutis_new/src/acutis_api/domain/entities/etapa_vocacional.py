import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import ForeignKey, UnicodeText, func
from sqlalchemy.orm import Mapped, mapped_column

from acutis_api.domain.database import table_registry


class PassosVocacionalEnum(str, Enum):
    pre_cadastro = 'pre_cadastro'
    cadastro = 'cadastro'
    ficha_vocacional = 'ficha_vocacional'


class PassosVocacionalStatusEnum(str, Enum):
    pendente = 'pendente'
    aprovado = 'aprovado'
    reprovado = 'reprovado'
    desistencia = 'desistencia'


@table_registry.mapped_as_dataclass
class EtapaVocacional:
    __tablename__ = 'etapas_vocacional'

    id: Mapped[uuid.UUID] = mapped_column(
        init=False, primary_key=True, default_factory=uuid.uuid4, index=True
    )
    fk_usuario_vocacional_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('usuarios_vocacional.id'), index=True, nullable=False
    )
    etapa: Mapped[PassosVocacionalEnum] = mapped_column(nullable=False)
    status: Mapped[PassosVocacionalStatusEnum] = mapped_column(nullable=False)
    justificativa: Mapped[str] = mapped_column(UnicodeText, nullable=True)
    fk_responsavel_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey('membros.id')
    )
    criado_em: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    atualizado_em: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )
