from dataclasses import dataclass
from datetime import date, datetime
from builder import db
from utils.functions import get_current_time


@dataclass
class CadastroVocacional(db.Model):
    __tablename__ = "cadastros_vocacional"

    id: int = db.Column(db.Integer, primary_key=True)
    fk_usuario_vocacional_id: int = db.Column(
        db.Integer,
        db.ForeignKey("usuarios_vocacional.id"),
        nullable=False,
        index=True,
        unique=True
    )
    fk_endereco_id: int = db.Column(
        db.Integer, db.ForeignKey("endereco.id"), nullable=False, index=True
    )
    data_nascimento: date = db.Column(db.Date, nullable=False)
    documento_identidade: str = db.Column(db.String(50), nullable=False, unique=True)
    created_at: datetime = db.Column(db.DateTime, default=get_current_time)
    updated_at: datetime = db.Column(db.DateTime)
