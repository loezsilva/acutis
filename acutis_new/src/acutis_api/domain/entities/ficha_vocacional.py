import uuid
from datetime import date, datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, UnicodeText, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from acutis_api.domain.database import table_registry

if TYPE_CHECKING:
    from acutis_api.domain.entities import (  # pragma: no cover
        SacramentoVocacional,
    )


@table_registry.mapped_as_dataclass
class FichaVocacional:
    __tablename__ = 'fichas_vocacional'

    id: Mapped[uuid.UUID] = mapped_column(
        init=False, primary_key=True, default_factory=uuid.uuid4, index=True
    )
    fk_usuario_vocacional_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('usuarios_vocacional.id'), index=True, unique=True
    )
    motivacao_instituto: Mapped[str] = mapped_column(
        String(255), nullable=False
    )
    motivacao_admissao_vocacional: Mapped[str] = mapped_column(
        String(255), nullable=False
    )
    referencia_conhecimento_instituto: Mapped[str] = mapped_column(
        String(255), nullable=False
    )
    identificacao_instituto: Mapped[str] = mapped_column(
        String(255), nullable=False
    )
    foto_vocacional: Mapped[str] = mapped_column(nullable=False)
    seminario_realizado_em: Mapped[date] = mapped_column(nullable=False)
    testemunho_conversao: Mapped[str] = mapped_column(
        UnicodeText, nullable=False
    )
    escolaridade: Mapped[str] = mapped_column(String(100), nullable=False)
    profissao: Mapped[str] = mapped_column(String(100), nullable=False)
    cursos: Mapped[str] = mapped_column(String(255), nullable=True)
    rotina_diaria: Mapped[str] = mapped_column(UnicodeText, nullable=False)
    aceitacao_familiar: Mapped[str] = mapped_column(
        UnicodeText, nullable=False
    )
    estado_civil: Mapped[str] = mapped_column(String(100), nullable=False)
    motivo_divorcio: Mapped[str] = mapped_column(String(255), nullable=True)
    deixou_religiao_anterior_em: Mapped[date] = mapped_column(nullable=True)
    remedio_controlado_inicio: Mapped[date] = mapped_column(nullable=True)
    remedio_controlado_termino: Mapped[date] = mapped_column(nullable=True)
    descricao_problema_saude: Mapped[str] = mapped_column(
        UnicodeText, nullable=True
    )
    criado_em: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    atualizado_em: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )

    sacramentos: Mapped['SacramentoVocacional'] = relationship(
        init=False, backref='ficha_vocacional', cascade='all, delete'
    )
