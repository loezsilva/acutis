from datetime import datetime
from typing import Dict

from sqlalchemy import func

from builder import db


class Progresso(db.Model):
    __tablename__ = "progresso"

    id: int = db.Column(db.Integer, primary_key=True)
    fk_usuario_id: int = db.Column(
        db.Integer, db.ForeignKey("usuario.id"), nullable=False
    )
    fk_aula_id: int = db.Column(
        db.Integer, db.ForeignKey("aula.id"), nullable=False
    )
    iniciado_em: datetime = db.Column(db.DateTime, default=func.now())
    concluido_em: datetime = db.Column(db.DateTime)

    def __repr__(self) -> str:
        return f"<Progresso (id={self.id})>"

    def to_dict(self) -> Dict:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
