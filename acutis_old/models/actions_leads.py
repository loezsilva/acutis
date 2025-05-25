from builder import db


class ActionsLeads(db.Model):
    __tablename__ = "actions_leads"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)
    titulo = db.Column(db.Unicode(255))
    descricao = db.Column(db.UnicodeText)
    background = db.Column(db.String(255))
    banner = db.Column(db.String(255))
    status = db.Column(db.Boolean)
    preenchimento_foto = db.Column(db.Boolean, default=False)
    label_foto = db.Column(db.String(100))
    sorteio = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime)
    cadastrado_por = db.Column(db.Integer, db.ForeignKey("usuario.id"))
    zone = db.Column(db.String(100))
    zone_id = db.Column(db.String(40))
