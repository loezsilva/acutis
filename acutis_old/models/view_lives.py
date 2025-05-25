from builder import db


class ViewLives(db.Model):
    __tablenames__ = "view_lives"

    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(100), nullable=False)
    fk_campanha_id = db.Column(db.Integer, db.ForeignKey("campanha.id"))
    rede_social = db.Column(db.String(50), nullable=False)
