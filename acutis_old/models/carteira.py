from datetime import datetime

from builder import db


class Carteira(db.Model):
    __tablename__ = "carteira"

    id = db.Column(db.Integer, primary_key=True)
    cod_carteira = db.Column(
        db.String(10), nullable=False, unique=True, index=True
    )
    fk_empresa_id = db.Column(
        db.Integer, db.ForeignKey("empresa.id"), nullable=False
    )
    fk_filial_id = db.Column(
        db.Integer, db.ForeignKey("filial.id"), nullable=False
    )
    fk_num_banco = db.Column(
        db.String(3), db.ForeignKey("banco.num_banco"), nullable=False
    )
    fk_num_agencia = db.Column(
        db.String(6), db.ForeignKey("agencia.num_agencia"), nullable=False
    )
    fk_num_conta = db.Column(
        db.String(6), db.ForeignKey("conta_corrente.num_conta"), nullable=False
    )
    descricao = db.Column(db.String(100), nullable=False)
    status = db.Column(db.SmallInteger, nullable=False)
    saldo_inicial = db.Column(db.Numeric(15, 4))
    database_saldo = db.Column(db.Numeric(15, 4))
    saldo_nao_compensado = db.Column(db.Numeric(15, 4))
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    usuario_criacao = db.Column(db.Integer, nullable=False)
    data_alteracao = db.Column(db.DateTime)
    usuario_alteracao = db.Column(db.Integer)
