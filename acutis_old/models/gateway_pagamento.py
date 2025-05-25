from datetime import datetime
from typing import List

from pydantic import BaseModel

from builder import db


class GatewayPagamento(db.Model):
    __tablename__ = "gateway_pagamento"

    id = db.Column(db.Integer, primary_key=True)
    fk_empresa_id = db.Column(
        db.Integer, db.ForeignKey("empresa.id"), nullable=False
    )
    descricao = db.Column(db.String(40), nullable=False)
    status = db.Column(db.SmallInteger)
    merchant_id = db.Column(db.String(20))
    merchant_key = db.Column(db.String(80))
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    usuario_criacao = db.Column(db.Integer, nullable=False)
    data_alteracao = db.Column(db.DateTime)
    usuario_alteracao = db.Column(db.Integer)

    def __repr__(self) -> str:
        return f"<GatewayPagamento: {self.id}>"


class PaymentGatewayCreateSchema(BaseModel):
    descricao: str
    status: bool
    merchant_id: str = None
    merchant_key: str = None


class UpdatePaymentSetup(BaseModel):
    credito_unico: int | str
    credito_recorrente: int | str
    pix_unico: int | str
    pix_recorrente: int | str
    boleto_unico: int | str
    boleto_recorrente: int | str


class ListGateway(BaseModel):
    id: int
    descricao: str

    class Config:
        orm_mode = True


class PaymentGatewayResponseSchema(BaseModel):
    list[ListGateway]


class GetCurrentPaymentSetup(UpdatePaymentSetup):

    class Config:
        orm_mode = True


class PaymentGatewayListResponseSchema(BaseModel):
    gateways_pagamento: List[PaymentGatewayResponseSchema]
    setup_pagamentos: GetCurrentPaymentSetup
