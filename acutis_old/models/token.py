from datetime import datetime

from builder import db


class Token(db.Model):
    __tablename__ = "tokens"

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(400), index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "token": self.token,
            "created_at": self.created_at,
        }

    def __repr__(self) -> str:
        return f"<Token {self.token}>"
