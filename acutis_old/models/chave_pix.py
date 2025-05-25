from datetime import datetime

from builder import db


class ChavePix(db.Model):
    __tablename__ = "chave_pix"

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
    chave = db.Column(db.String(100))
    tipo_chave = db.Column(db.SmallInteger)
    principal = db.Column(db.SmallInteger)
    status = db.Column(db.SmallInteger)
    cedente = db.Column(db.String(50))
    cnpj_cedente = db.Column(db.String(20))
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    usuario_criacao = db.Column(db.Integer, nullable=False)
    data_alteracao = db.Column(db.DateTime)
    usuario_alteracao = db.Column(db.Integer)
