from dataclasses import dataclass
from datetime import datetime

from builder import db
from utils.functions import get_current_time


@dataclass
class FamiliaAgape(db.Model):
    __tablename__ = "familia_agape"

    id: int = db.Column(db.Integer, primary_key=True)
    fk_endereco_id: int = db.Column(
        db.Integer, db.ForeignKey("endereco.id"), nullable=False, index=True
    )
    nome_familia: str = db.Column(db.String(100), nullable=False, index=True)
    status: bool = db.Column(db.Boolean, index=True)
    observacao: str = db.Column(db.String(255))
    comprovante_residencia: str | None = db.Column(db.String(100))
    deleted_at: datetime = db.Column(db.DateTime)
    created_at: datetime = db.Column(
        db.DateTime, default=get_current_time, index=True
    )
    updated_at: datetime = db.Column(db.DateTime)
    cadastrada_por: int = db.Column(
        db.Integer, db.ForeignKey("usuario.id"), index=True
    )
    membros = db.relationship(
        "MembroAgape", backref="familia", lazy="dynamic", cascade="all, delete"
    )

    def __repr__(self) -> str:
        return f"<FamiliaAgape: {self.id}>"
