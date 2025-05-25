from dataclasses import dataclass
from datetime import datetime
from builder import db
from utils.functions import get_current_time


@dataclass
class ItemDoacaoAgape(db.Model):
    __tablename__ = "item_doacao_agape"

    id: int = db.Column(db.Integer, primary_key=True)
    fk_item_instancia_agape_id: int = db.Column(
        db.Integer,
        db.ForeignKey("item_instancia_agape.id"),
        nullable=False,
        index=True,
    )
    fk_doacao_agape_id: int = db.Column(
        db.Integer,
        db.ForeignKey("doacao_agape.id"),
        nullable=False,
        index=True,
    )
    quantidade: int = db.Column(db.Integer, nullable=False)
    created_at: datetime = db.Column(db.DateTime, default=get_current_time)
    updated_at: datetime = db.Column(db.DateTime)
