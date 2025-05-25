from dataclasses import dataclass
from datetime import datetime
from typing import Dict

from sqlalchemy import func

from builder import db


@dataclass
class Modulo(db.Model):
    __tablename__ = "modulo"

    id: int = db.Column(db.Integer, primary_key=True)
    nome: str = db.Column(db.String(100), nullable=False)
    fk_curso_id: int = db.Column(
        db.Integer, db.ForeignKey("curso.id"), nullable=False
    )
    data_criacao: datetime = db.Column(db.DateTime, default=func.now())
    usuario_criacao: int = db.Column(
        db.Integer, db.ForeignKey("usuario.id"), nullable=False
    )
    data_alteracao: datetime = db.Column(db.DateTime)
    usuario_alteracao: int = db.Column(db.Integer, db.ForeignKey("usuario.id"))

    aulas = db.relationship(
        "Aula", backref="modulo", lazy="dynamic", cascade="all, delete"
    )

    def __repr__(self) -> str:
        return f"<Modulo: (id={self.id}, nome={self.nome})>"

    def to_dict(self) -> Dict:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
