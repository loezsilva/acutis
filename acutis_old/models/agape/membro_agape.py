from dataclasses import dataclass
from datetime import date, datetime

from builder import db
from utils.functions import get_current_time


@dataclass
class MembroAgape(db.Model):
    __tablename__ = "membro_agape"

    id: int = db.Column(db.Integer, primary_key=True)
    fk_familia_agape_id: int = db.Column(
        db.Integer,
        db.ForeignKey("familia_agape.id"),
        nullable=False,
        index=True,
    )
    responsavel: bool = db.Column(db.Boolean, index=True)
    nome: str = db.Column(db.String(100), nullable=False)
    email: str = db.Column(db.String(100))
    telefone: str = db.Column(db.String(20))
    cpf: str = db.Column(db.String(14), index=True)
    data_nascimento: date = db.Column(db.Date, nullable=False, index=True)
    funcao_familiar: str = db.Column(db.String(50), nullable=False)
    escolaridade: str = db.Column(db.String(50), nullable=False)
    ocupacao: str = db.Column(db.String(100), nullable=False)
    renda: float | None = db.Column(db.Numeric(15, 2))
    foto_documento: str | None = db.Column(db.String(100))
    beneficiario_assistencial: bool = db.Column(db.Boolean, index=True)
    created_at: datetime = db.Column(
        db.DateTime, default=get_current_time, index=True
    )
    updated_at: datetime = db.Column(db.DateTime)

    def __repr__(self) -> str:
        return f"<MembroAgape: {self.id}>"
