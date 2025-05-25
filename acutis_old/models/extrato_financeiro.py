from datetime import datetime

from builder import db


class ExtratoFinanceiro(db.Model):
    __tablename__ = "extrato_financeiro"

    id = db.Column(db.Integer, primary_key=True)
    fk_empresa_id = db.Column(
        db.Integer, db.ForeignKey("empresa.id"), nullable=False
    )
    fk_filial_id = db.Column(
        db.Integer, db.ForeignKey("filial.id"), nullable=False
    )
    fk_carteira_cod = db.Column(
        db.String(10), db.ForeignKey("carteira.cod_carteira"), nullable=False
    )
    fk_lancamento_id = db.Column(
        db.Integer, db.ForeignKey("lancamento.id"), nullable=False
    )
    fk_forma_pagamento_id = db.Column(
        db.Integer, db.ForeignKey("forma_pagamento.id"), nullable=False
    )
    numero_documento = db.Column(db.String(40), nullable=False)
    tipo = db.Column(db.SmallInteger, nullable=False)
    status_extrato = db.Column(db.SmallInteger, nullable=False)
    status_conciliacao = db.Column(db.SmallInteger, nullable=False)
    historico = db.Column(db.String(255))
    data_baixa = db.Column(db.DateTime, nullable=False)
    data_cancelamento_baixa = db.Column(db.DateTime)
    valor = db.Column(db.Numeric(15, 4), nullable=False)
    data_extrato = db.Column(db.DateTime, nullable=False)
    data_vencimento = db.Column(db.DateTime)
    data_compensacao = db.Column(db.DateTime)
    data_cancelamento = db.Column(db.DateTime)
    data_estorno = db.Column(db.DateTime)
    status_concil_cartao = db.Column(db.SmallInteger)
    cartao_operadora = db.Column(db.Integer)
    cartao_bandeira = db.Column(db.Integer)
    cartao_nsu = db.Column(db.String(50))
    cartao_tid = db.Column(db.String(50))
    cartao_autorizacao = db.Column(db.String(50))
    cartao_numero_parcela = db.Column(db.Integer)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    usuario_criacao = db.Column(db.Integer, nullable=False)
    data_alteracao = db.Column(db.DateTime)
    usuario_alteracao = db.Column(db.Integer)
