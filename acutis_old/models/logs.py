from datetime import datetime
from dataclasses import dataclass

from builder import db


@dataclass
class Logs(db.Model):
    __tablename__ = "logs"

    id: int = db.Column(db.BigInteger, primary_key=True)
    usuario_id: int = db.Column(
        db.Integer, db.ForeignKey("usuario.id"), nullable=False
    )
    mensagem: str = db.Column(db.UnicodeText, nullable=False)
    level: int = db.Column(db.Integer, nullable=False)
    tipo: int = db.Column(db.Integer, nullable=False)
    acao: int = db.Column(db.Integer, nullable=False)
    criado_em: datetime = db.Column(
        db.DateTime, default=datetime.now(), nullable=False
    )
