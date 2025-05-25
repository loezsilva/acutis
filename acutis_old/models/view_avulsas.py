from builder import db


class ViewAvulsas(db.Model):
    __tablename__ = "view_avulsas"

    id = db.Column(db.Integer, primary_key=True)
    data_hora_inicio = db.Column(db.DateTime, nullable=False)
    fk_view_live_id = db.Column(db.Integer, db.ForeignKey("view_lives.id"))
