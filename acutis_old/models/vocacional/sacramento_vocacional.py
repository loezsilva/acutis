from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from builder import db
from utils.functions import get_current_time


class VocationalSacramentsEnum(str, Enum):
    BATISMO = "batismo"
    CRISMA = "crisma"
    EUCARISTIA = "eucaristia"
    PENITENCIA = "penitencia"
    UNCAO_DOS_ENFERMOS = "uncao_dos_enfermos"
    ORDEM = "ordem"
    MATRIMONIO = "matrimonio"


@dataclass
class SacramentoVocacional(db.Model):
    __tablename__ = "sacramentos_vocacional"

    id: int = db.Column(db.Integer, primary_key=True)
    fk_ficha_vocacional_id: int = db.Column(
        db.Integer,
        db.ForeignKey("fichas_vocacional.id"),
        nullable=False,
        index=True,
    )
    nome: VocationalSacramentsEnum = db.Column(db.String(20), nullable=False)
    created_at: datetime = db.Column(db.DateTime, default=get_current_time)
    updated_at: datetime = db.Column(db.DateTime)
