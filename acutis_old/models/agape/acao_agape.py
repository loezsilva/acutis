from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from builder import db
from utils.functions import get_current_time


class PerfisAgape(str, Enum):
    Voluntario = "Voluntario Agape"
    Administrador = "Administrador Agape"


@dataclass
class AcaoAgape(db.Model):
    __tablename__ = "acao_agape"

    id: int = db.Column(db.Integer, primary_key=True)
    nome: str = db.Column(db.String, nullable=False)
    created_at: datetime = db.Column(
        db.DateTime, default=get_current_time, index=True
    )
    updated_at: datetime = db.Column(db.DateTime)

    def __repr__(self) -> str:
        return f"<AcaoAgape: {self.id}>"
