from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from builder import db


class SetupPagamento(db.Model):
    __tablename__ = "setup_pagamento"

    id = db.Column(db.Integer, primary_key=True)
    fk_campanha_id = db.Column(
        db.Integer, db.ForeignKey("campanha.id"), unique=True
    )
    credito_unico = db.Column(
        db.Integer, db.ForeignKey("gateway_pagamento.id")
    )
    credito_recorrente = db.Column(
        db.Integer, db.ForeignKey("gateway_pagamento.id")
    )
    pix_unico = db.Column(db.Integer, db.ForeignKey("gateway_pagamento.id"))
    pix_recorrente = db.Column(
        db.Integer, db.ForeignKey("gateway_pagamento.id")
    )
    boleto_unico = db.Column(db.Integer, db.ForeignKey("gateway_pagamento.id"))
    boleto_recorrente = db.Column(
        db.Integer, db.ForeignKey("gateway_pagamento.id")
    )
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    usuario_criacao = db.Column(db.Integer)
    data_alteracao = db.Column(db.DateTime)
    usuario_alteracao = db.Column(db.Integer)

    def to_dict(self):
        not_return = [
            "data_criacao",
            "usuario_criacao",
            "data_alteracao",
            "usuario_alteracao",
        ]
        return {
            c.name: getattr(self, c.name)
            for c in self.__table__.columns
            if c.name not in not_return
        }


class SetupPagamentoSchema(BaseModel):
    id: Optional[int]
    fk_campanha_id: Optional[int]
    credito_unico: Optional[int]
    credito_recorrente: Optional[int]
    pix_unico: Optional[int]
    pix_recorrente: Optional[int]
    boleto_unico: Optional[int]
    boleto_recorrente: Optional[int]

    class Config:
        orm_mode = True
