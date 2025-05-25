from datetime import datetime

from builder import db


class TipoDocumento(db.Model):
    __tablename__ = "tipo_documento"

    id = db.Column(db.Integer, primary_key=True)
    fk_empresa_id = db.Column(
        db.Integer, db.ForeignKey("empresa.id"), nullable=False
    )
    descricao = db.Column(db.String(40))
    ultimo_numero = db.Column(db.String(20))
    serie_documento = db.Column(db.String(8))
    status = db.Column(db.SmallInteger)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    usuario_criacao = db.Column(db.Integer, nullable=False)
    data_alteracao = db.Column(db.DateTime)
    usuario_alteracao = db.Column(db.Integer)
