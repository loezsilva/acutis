from dataclasses import dataclass
from builder import db


@dataclass
class LogLocalidade(db.Model):
    __tablename__ = "log_localidade"

    loc_nu: int = db.Column(db.Integer, primary_key=True)
    ufe_sg: str = db.Column(db.String(2))
    loc_no: str = db.Column(db.String(72))
    cep: str = db.Column(db.String(8))
    loc_in_sit: str = db.Column(db.String(1))
    loc_in_tipo_loc: str = db.Column(db.String(1))
    loc_nu_sub: int = db.Column(db.Integer)
    loc_no_abrev: str = db.Column(db.String(36))
    mun_nu: int = db.Column(db.Integer)
