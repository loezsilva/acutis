from builder import db
from utils.functions import get_current_time


class ViewAudiencias(db.Model):
    __tablename__ = "view_audiencias"

    id = db.Column(db.Integer, primary_key=True)
    fk_view_live_id = db.Column(db.Integer, db.ForeignKey("view_lives.id"))
    titulo = db.Column(db.String(255), nullable=False)
    data_hora_registro = db.Column(db.DateTime, default=get_current_time)
    audiencia = db.Column(db.Integer, nullable=False)
