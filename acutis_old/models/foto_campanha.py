from datetime import datetime
from builder import db


class FotoCampanha(db.Model):
    __tablename__ = "foto_campanha"

    id = db.Column(db.Integer, primary_key=True)
    fk_campanha_id = db.Column(db.Integer, db.ForeignKey("campanha.id"))
    fk_usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"))
    foto = db.Column(db.String(100))
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    usuario_criacao = db.Column(db.Integer, nullable=False)
    data_alteracao = db.Column(db.DateTime)
    usuario_alteracao = db.Column(db.Integer)
