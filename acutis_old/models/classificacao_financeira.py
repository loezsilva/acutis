from datetime import datetime

from builder import db


class ClassificacaoFinanceira(db.Model):
    __tablename__ = "classificacao_financeira"

    id = db.Column(db.Integer, primary_key=True)
    id_classificacao_financeira = db.Column(
        db.String(25), nullable=False, unique=True, index=True
    )
    fk_empresa_id = db.Column(
        db.Integer, db.ForeignKey("empresa.id"), nullable=False
    )
    descricao = db.Column(db.String(40), nullable=False)
    permite_lancamento = db.Column(db.Boolean, nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    usuario_criacao = db.Column(db.Integer, nullable=False)
    data_alteracao = db.Column(db.DateTime)
    usuario_alteracao = db.Column(db.Integer)
