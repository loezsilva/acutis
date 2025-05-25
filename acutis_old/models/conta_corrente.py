from datetime import datetime

from builder import db


class ContaCorrente(db.Model):
    __tablename__ = "conta_corrente"

    id = db.Column(db.Integer, primary_key=True)
    fk_empresa_id = db.Column(
        db.Integer, db.ForeignKey("empresa.id"), nullable=False
    )
    fk_num_banco = db.Column(
        db.String(3), db.ForeignKey("banco.num_banco"), nullable=False
    )
    fk_num_agencia = db.Column(
        db.String(6), db.ForeignKey("agencia.num_agencia"), nullable=False
    )
    num_conta = db.Column(db.String(6), nullable=False, unique=True)
    digito_conta = db.Column(db.String(2))
    tipo_conta = db.Column(db.SmallInteger, nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    usuario_criacao = db.Column(db.Integer, nullable=False)
    data_alteracao = db.Column(db.DateTime)
    usuario_alteracao = db.Column(db.Integer)
