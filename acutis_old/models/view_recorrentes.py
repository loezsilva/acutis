from builder import db


class ViewRecorrentes(db.Model):
    __tablename__ = "view_recorrentes"

    id = db.Column(db.Integer, primary_key=True)
    dia_semana = db.Column(db.String(50), nullable=False)
    data_hora_inicio = db.Column(db.Time, nullable=False)
    fk_view_live_id = db.Column(db.Integer, db.ForeignKey("view_lives.id"))
