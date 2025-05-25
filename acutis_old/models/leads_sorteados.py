from builder import db
from utils.functions import get_current_time


class LeadsSorteados(db.Model):
    __tablename__ = "leads_sorteados"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String)
    email = db.Column(db.String)
    data_sorteio = db.Column(db.DateTime)
    sorteador = db.Column(db.Integer, db.ForeignKey("usuario.id"))
    acao_sorteada = db.Column(db.Integer, db.ForeignKey("actions_leads.id"))
    data_criacao = db.Column(db.DateTime, default=get_current_time)
