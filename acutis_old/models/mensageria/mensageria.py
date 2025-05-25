from builder import db
from datetime import datetime
from dataclasses import dataclass


@dataclass
class Mensageria(db.Model):
    __tablename__ = "mensageria"

    id: int = db.Column(db.Integer, primary_key=True)
    sg_message_id: str = db.Column(db.String(150), nullable=False, index=True)
    email: str = db.Column(db.String(100), nullable=False, index=True)
    fk_tipo_email_id: int = db.Column(
        db.Integer, db.ForeignKey("tipo_email.id"), nullable=False
    )
    status: str = db.Column(db.String(25))
    url: str = db.Column(db.Text)
    updated_at: datetime = db.Column(db.DateTime, nullable=True)
    created_at: datetime = db.Column(db.DateTime, nullable=False)
    motivo_retorno: str = db.Column(db.String(1000), nullable=True)
    tipo_email = db.relationship("TipoEmail", cascade="all", backref="mensageria")
