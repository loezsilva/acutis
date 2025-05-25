from datetime import datetime

from builder import db


class BaixaLancamento(db.Model):
    __tablename__ = "baixa_lancamento"

    id = db.Column(db.Integer, primary_key=True)
    fk_empresa_id = db.Column(
        db.Integer, db.ForeignKey("empresa.id"), nullable=False
    )
    fk_lancamento_id = db.Column(
        db.Integer, db.ForeignKey("lancamento.id"), nullable=False
    )
    fk_forma_pagamento_id = db.Column(
        db.Integer, db.ForeignKey("forma_pagamento.id"), nullable=False
    )
    fk_extrato_financeiro_id = db.Column(
        db.Integer, db.ForeignKey("extrato_financeiro.id")
    )
    fk_carteira_cod = db.Column(
        db.String(10), db.ForeignKey("carteira.cod_carteira"), nullable=False
    )
    data_baixa = db.Column(db.DateTime, nullable=False)
    data_cancelamento_baixa = db.Column(db.DateTime)
    valor_baixa = db.Column(db.Numeric(15, 4), nullable=False)
    valor_original = db.Column(db.Numeric(15, 4), nullable=False)
    valor_desconto = db.Column(db.Numeric(15, 4))
    valor_juros = db.Column(db.Numeric(15, 4))
    valor_multa = db.Column(db.Numeric(15, 4))
    status_baixa = db.Column(db.SmallInteger)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    usuario_criacao = db.Column(db.Integer, nullable=False)
    data_alteracao = db.Column(db.DateTime)
    usuario_alteracao = db.Column(db.Integer)
