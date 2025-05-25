from datetime import datetime

from builder import db


class Agencia(db.Model):
    __tablename__ = "agencia"

    id = db.Column(db.Integer, primary_key=True)
    fk_num_banco = db.Column(
        db.String(3), db.ForeignKey("banco.num_banco"), nullable=False
    )
    fk_municipio_id = db.Column(db.Integer, db.ForeignKey("municipio.id"))
    fk_estado_id = db.Column(db.Integer, db.ForeignKey("estado.id"))
    fk_pais_id = db.Column(db.Integer, db.ForeignKey("pais.id"))
    num_agencia = db.Column(
        db.String(6), nullable=False, unique=True, index=True
    )
    nome = db.Column(db.String(60))
    nome_reduzido = db.Column(db.String(20))
    numero_oficial = db.Column(db.String(3), nullable=False)
    digito_banco = db.Column(db.String(1))
    rua = db.Column(db.String(100))
    numero = db.Column(db.String(8))
    complemento = db.Column(db.String(60))
    bairro = db.Column(db.String(80))
    cidade = db.Column(db.String(32))
    cep = db.Column(db.String(9))
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    usuario_criacao = db.Column(db.Integer, nullable=False)
    data_alteracao = db.Column(db.DateTime)
    usuario_alteracao = db.Column(db.Integer)
