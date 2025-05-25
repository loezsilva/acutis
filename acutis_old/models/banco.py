from datetime import datetime

from builder import db


class Banco(db.Model):
    __tablename__ = "banco"

    id = db.Column(db.Integer, primary_key=True)
    num_banco = db.Column(
        db.String(3), nullable=False, unique=True, index=True
    )
    nome = db.Column(db.String(40))
    nome_reduzido = db.Column(db.String(20))
    numero_oficial = db.Column(db.String(3), nullable=False)
    digito_banco = db.Column(db.String(1))
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    usuario_criacao = db.Column(db.Integer, nullable=False)
    data_alteracao = db.Column(db.DateTime)
    usuario_alteracao = db.Column(db.Integer)
