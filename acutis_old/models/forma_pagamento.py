from dataclasses import dataclass
from datetime import datetime

from builder import db
from utils.functions import get_current_time


@dataclass
class FormaPagamento(db.Model):
    __tablename__ = "forma_pagamento"

    id: int = db.Column(db.Integer, primary_key=True)
    fk_empresa_id: int = db.Column(db.Integer, db.ForeignKey("empresa.id"))
    descricao: str = db.Column(db.String(40))
    tipo_forma_pagamento: int = db.Column(db.SmallInteger)
    taxa_admin: float = db.Column(db.Numeric(15, 4))
    taxa_admin_parc: float = db.Column(db.Numeric(15, 4))
    status: int = db.Column(db.SmallInteger)
    data_criacao: datetime = db.Column(db.DateTime, default=get_current_time)
    usuario_criacao: int = db.Column(db.Integer, nullable=False)
    data_alteracao: datetime = db.Column(db.DateTime)
    usuario_alteracao: int = db.Column(db.Integer)
