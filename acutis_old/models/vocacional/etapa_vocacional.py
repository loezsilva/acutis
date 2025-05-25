from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from builder import db
from utils.functions import get_current_time


class VocationalStepsEnum(str, Enum):
    PRE_CADASTRO = "pre_cadastro"
    CADASTRO = "cadastro"
    FICHA_VOCACIONAL = "ficha_vocacional"


class VocationalStepsStatusEnum(str, Enum):
    PENDENTE = "pendente"
    APROVADO = "aprovado"
    REPROVADO = "reprovado"
    DESISTENCIA = "desistencia"


@dataclass
class EtapaVocacional(db.Model):
    __tablename__ = "etapas_vocacional"

    id: int = db.Column(db.Integer, primary_key=True)
    fk_usuario_vocacional_id: int = db.Column(
        db.Integer,
        db.ForeignKey("usuarios_vocacional.id"),
        nullable=False,
        index=True,
    )
    etapa: VocationalStepsEnum = db.Column(
        db.String(20), nullable=False, index=True
    )
    status: VocationalStepsStatusEnum = db.Column(
        db.String(20), nullable=False, index=True
    )
    justificativa: str = db.Column(db.Text)
    responsavel: int = db.Column(
        db.Integer, db.ForeignKey("usuario.id"), index=True
    )
    created_at: datetime = db.Column(
        db.DateTime, default=get_current_time, index=True
    )
    updated_at: datetime = db.Column(db.DateTime)
