from dataclasses import dataclass
from datetime import datetime

from builder import db
from utils.functions import get_current_time


@dataclass
class EstoqueAgape(db.Model):
    __tablename__ = "estoque_agape"

    id: int = db.Column(db.Integer, primary_key=True)
    item: str = db.Column(db.String(100), nullable=False, index=True)
    quantidade: int = db.Column(db.Integer, nullable=False)
    created_at: datetime = db.Column(
        db.DateTime, default=get_current_time, index=True
    )
    updated_at: datetime = db.Column(db.DateTime)

    def __repr__(self) -> str:
        return f"<EstoqueAgape: {self.id}>"
