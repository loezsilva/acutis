from builder import db
from utils.functions import get_current_time


class FotoLeads(db.Model):
    __tablename__ = "foto_leads"

    id = db.Column(db.Integer, primary_key=True)
    fk_action_lead_id = db.Column(
        db.Integer, db.ForeignKey("actions_leads.id")
    )
    fk_user_import_id = db.Column(
        db.Integer, db.ForeignKey("users_imports.id")
    )
    foto = db.Column(db.String(100))
    data_criacao = db.Column(db.DateTime, default=get_current_time)
    data_alteracao = db.Column(db.DateTime)
    data_download = db.Column(db.DateTime, nullable=True)
    user_download = db.Column(db.Integer)
