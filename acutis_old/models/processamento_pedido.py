from dataclasses import dataclass
from datetime import datetime

from builder import db
from utils.functions import get_current_time


@dataclass
class ProcessamentoPedido(db.Model):
    __tablename__ = "processamento_pedido"

    id: int = db.Column(db.Integer, primary_key=True)
    fk_empresa_id: int = db.Column(db.Integer, db.ForeignKey("empresa.id"))
    fk_filial_id: int = db.Column(db.Integer, db.ForeignKey("filial.id"))
    fk_pedido_id: int = db.Column(
        db.Integer, db.ForeignKey("pedido.id"), nullable=False, index=True
    )
    fk_clifor_id: int = db.Column(
        db.Integer, db.ForeignKey("clifor.id"), nullable=False, index=True
    )
    fk_forma_pagamento_id: int = db.Column(
        db.Integer,
        db.ForeignKey("forma_pagamento.id"),
        nullable=False,
        index=True,
    )
    fk_lancamento_id: int = db.Column(
        db.Integer, db.ForeignKey("lancamento.id")
    )
    data_processamento: datetime = db.Column(
        db.DateTime, nullable=False, index=True
    )
    valor: float = db.Column(db.Numeric(15, 4), nullable=False)
    status_processamento: int = db.Column(db.SmallInteger, index=True)
    id_transacao_gateway: str = db.Column(db.String(255))
    transaction_id: str = db.Column(db.String(100))
    id_pagamento: str = db.Column(db.String(100))
    contabilizar_doacao: bool = db.Column(db.Boolean, default=True, index=True)
    nosso_numero: str = db.Column(db.String(12))
    data_lembrete_doacao: datetime = db.Column(db.DateTime)
    lembrete_enviado_por: int = db.Column(
        db.Integer, db.ForeignKey("usuario.id")
    )
    data_criacao: datetime = db.Column(db.DateTime, default=get_current_time)
    usuario_criacao: int = db.Column(db.Integer, nullable=False)
    data_alteracao: datetime = db.Column(db.DateTime)
    usuario_alteracao: int = db.Column(db.Integer)
