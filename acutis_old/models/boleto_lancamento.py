from datetime import datetime

from builder import db


class BoletoLancamento(db.Model):
    __tablename__ = "boleto_lancamento"

    id = db.Column(db.Integer, primary_key=True)
    fk_empresa_id = db.Column(
        db.Integer, db.ForeignKey("empresa.id"), nullable=False
    )
    fk_lancamento_id = db.Column(
        db.Integer, db.ForeignKey("lancamento.id"), nullable=False
    )
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    usuario_criacao = db.Column(db.Integer, nullable=False)
    data_alteracao = db.Column(db.DateTime)
    usuario_alteracao = db.Column(db.Integer)
