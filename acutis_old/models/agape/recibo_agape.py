from dataclasses import dataclass
from datetime import datetime

from builder import db
from utils.functions import get_current_time


@dataclass
class ReciboAgape(db.Model):
    __tablename__ = "recibo_agape"

    id: int = db.Column(db.Integer, primary_key=True)
    fk_doacao_agape_id: int = db.Column(
        db.Integer, db.ForeignKey("doacao_agape.id"), index=True
    )
    recibo: str = db.Column(db.String(100))
    created_at: datetime = db.Column(db.DateTime, default=get_current_time)
    updated_at: datetime = db.Column(db.DateTime)

    def __repr__(self) -> str:
        return f"<ReciboAgape: {self.id}>"
