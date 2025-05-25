import uuid
from datetime import date

from sqlalchemy import (
    ForeignKey,
    Numeric,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column

from acutis_api.domain.database import table_registry
from acutis_api.domain.entities.modelo_base import ModeloBase


@table_registry.mapped_as_dataclass
class MembroAgape(ModeloBase):
    __tablename__ = 'membros_agape'

    fk_familia_agape_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('familias_agape.id'), index=True
    )
    responsavel: Mapped[bool] = mapped_column(index=True)
    nome: Mapped[str]
    email: Mapped[str | None]
    telefone: Mapped[str | None]
    cpf: Mapped[str | None] = mapped_column(String(14), index=True)
    data_nascimento: Mapped[date] = mapped_column(index=True)
    funcao_familiar: Mapped[str]
    escolaridade: Mapped[str]
    ocupacao: Mapped[str]
    renda: Mapped[float | None] = mapped_column(Numeric(15, 2))
    foto_documento: Mapped[str | None]
    beneficiario_assistencial: Mapped[bool] = mapped_column(index=True)
