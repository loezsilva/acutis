from datetime import datetime

from sqlalchemy import func

from builder import db


class Matricula(db.Model):
    __tablename__ = "matricula"

    id: int = db.Column(db.Integer, primary_key=True)
    fk_curso_id: int = db.Column(db.Integer, db.ForeignKey("curso.id"))
    fk_progresso_id: int = db.Column(db.Integer, db.ForeignKey("progresso.id"))
    matriculado_em: datetime = db.Column(db.DateTime, default=func.now())
