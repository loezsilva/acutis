from dataclasses import dataclass
from datetime import datetime
from builder import db
from utils.functions import get_current_time

@dataclass
class FotoFamiliaAgape(db.Model):
    __tablename__ = 'fotos_familias_agape'

    id: int = db.Column(db.Integer, primary_key=True)
    fk_familia_agape_id: int = db.Column(
        db.Integer, 
        db.ForeignKey('familia_agape.id'), 
        index=True, 
        nullable=False
    )
    foto: str = db.Column(db.String(100), nullable=False)
    criado_em: datetime = db.Column(
        db.DateTime, default=get_current_time, index=True
    )
    atualizado_em: datetime = db.Column(db.DateTime)