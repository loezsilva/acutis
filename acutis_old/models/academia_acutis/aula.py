from datetime import datetime
from typing import Dict

from sqlalchemy import func

from builder import db


class Aula(db.Model):
    __tablename__ = "aula"

    id: int = db.Column(db.Integer, primary_key=True)
    titulo: str = db.Column(db.String(100), nullable=False)
    carga_horaria: float = db.Column(db.Float, nullable=False)
    link_video: str = db.Column(db.UnicodeText)
    material_apoio: str = db.Column(db.UnicodeText)
    texto: str = db.Column(db.UnicodeText)
    fk_modulo_id: int = db.Column(
        db.Integer, db.ForeignKey("modulo.id"), nullable=False
    )
    data_criacao: datetime = db.Column(db.DateTime, default=func.now())
    usuario_criacao: int = db.Column(
        db.Integer, db.ForeignKey("usuario.id"), nullable=False
    )
    data_alteracao: datetime = db.Column(db.DateTime)
    usuario_alteracao: int = db.Column(db.Integer, db.ForeignKey("usuario.id"))

    def __repr__(self) -> str:
        return f"<Aula: (id={self.id}, titulo={self.titulo})>"

    def to_dict(self) -> Dict:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
