from builder import db
from datetime import datetime
import pytz


class TipoEmail(db.Model):
    id: int = db.Column(db.Integer, primary_key=True, index=True)
    slug: str = db.Column(db.String(150), nullable=True, unique=True)
    created_at: datetime = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.now(pytz.timezone("America/Fortaleza")),
    )
    updated_at: datetime = db.Column(db.DateTime, nullable=True)
