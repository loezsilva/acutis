from datetime import datetime

from builder import db


class Convenio(db.Model):
    __tablename__ = "convenio"

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
    fk_num_conta = db.Column(
        db.String(6), db.ForeignKey("conta_corrente.num_conta"), nullable=False
    )
    convenio = db.Column(db.String(20))
    digito_convenio = db.Column(db.String(2))
    carteira = db.Column(db.String(3))
    tipo_carteira = db.Column(db.SmallInteger)
    cedente = db.Column(db.String(50))
    cnpj_cedente = db.Column(db.String(20))
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    usuario_criacao = db.Column(db.Integer, nullable=False)
    data_alteracao = db.Column(db.DateTime)
    usuario_alteracao = db.Column(db.Integer)
