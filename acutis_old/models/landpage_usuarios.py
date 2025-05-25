from dataclasses import dataclass
from datetime import datetime
from builder import db
from utils.functions import get_current_time


@dataclass
class LandpageUsers(db.Model):
    __tablename__ = "landpage_users"

    user_id: int = db.Column(
        db.Integer, db.ForeignKey("usuario.id"), primary_key=True
    )
    landpage_id: int = db.Column(db.Integer, db.ForeignKey("landpage.id"))
    campaign_id: int = db.Column(db.Integer, db.ForeignKey("campanha.id"))
    clifor_id: int = db.Column(db.Integer, db.ForeignKey("clifor.id"))
    registered_at: datetime = db.Column(db.DateTime, default=get_current_time)

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "landpage_id": self.landpage_id,
            "clifor_id": self.clifor_id,
            "campaign_id": self.campaign_id,
            "registered_at": self.registered_at,
        }

    def __repr__(self) -> str:
        return f"LandpageUsers: {self.clifor_id}"
