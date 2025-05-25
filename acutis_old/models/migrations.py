from dataclasses import dataclass
from builder import db


@dataclass
class Migrations(db.Model):
    __tablename__ = "migrations"

    id: int = db.Column(db.Integer, primary_key=True)
    migration: str = db.Column(db.UnicodeText(255), nullable=False)
    batch: int = db.Column(db.Integer, nullable=False)
