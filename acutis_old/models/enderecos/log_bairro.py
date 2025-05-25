from dataclasses import dataclass
from builder import db


@dataclass
class LogBairro(db.Model):
    __tablename__ = "log_bairro"

    bai_nu: int = db.Column(db.Integer, primary_key=True)
    ufe_sg: str = db.Column(db.String(2), nullable=False)
    loc_nu: int = db.Column(db.Integer, nullable=False)
    bai_no: str = db.Column(db.String(72), nullable=False)
    bai_no_abrev: str = db.Column(db.String(36))
