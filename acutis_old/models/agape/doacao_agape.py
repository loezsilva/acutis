from dataclasses import dataclass
from datetime import datetime

from builder import db
from utils.functions import get_current_time


@dataclass
class DoacaoAgape(db.Model):
    __tablename__ = "doacao_agape"

    id: int = db.Column(db.Integer, primary_key=True)
    fk_familia_agape_id: int = db.Column(
        db.Integer,
        db.ForeignKey("familia_agape.id"),
        nullable=False,
        index=True,
    )
    created_at: datetime = db.Column(
        db.DateTime, default=get_current_time, index=True
    )
    updated_at: datetime = db.Column(db.DateTime)

    def __repr__(self) -> str:
        return f"<DoacaoAgape: {self.id}>"
