from dataclasses import dataclass
from datetime import datetime

from builder import db
from utils.functions import get_current_time


@dataclass
class AquisicaoAgape(db.Model):
    __tablename__ = "aquisicao_agape"

    id: int = db.Column(db.Integer, primary_key=True)
    fk_estoque_agape_id: int = db.Column(
        db.Integer,
        db.ForeignKey("estoque_agape.id"),
        nullable=False,
        index=True,
    )
    quantidade: int = db.Column(db.Integer, nullable=False)
    created_at: datetime = db.Column(db.DateTime, default=get_current_time)
    updated_at: datetime = db.Column(db.DateTime)

    def __repr__(self) -> str:
        return f"<AquisicaoAgape: {self.id}>"
