from dataclasses import dataclass
from datetime import datetime
from typing import Dict

from sqlalchemy import func

from builder import db


@dataclass
class Curso(db.Model):
    __tablename__ = "curso"

    id: int = db.Column(db.Integer, primary_key=True)
    nome: str = db.Column(db.String(80), nullable=False)
    descricao: str = db.Column(db.UnicodeText, nullable=False)
    imagem: str = db.Column(db.UnicodeText, nullable=False)
    preco: float = db.Column(db.Float, nullable=False)
    status: bool = db.Column(db.Boolean, nullable=False)
    data_criacao: datetime = db.Column(db.DateTime, default=func.now())
    usuario_criacao: int = db.Column(
        db.Integer, db.ForeignKey("usuario.id"), nullable=False
    )
    data_alteracao: datetime = db.Column(db.DateTime)
    usuario_alteracao: int = db.Column(db.Integer, db.ForeignKey("usuario.id"))

    modulos = db.relationship(
        "Modulo", backref="curso", lazy="dynamic", cascade="all, delete"
    )

    def __repr__(self) -> str:
        return f"<Curso: (id={self.id}, nome={self.nome})>"

    def to_dict(self) -> Dict:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
