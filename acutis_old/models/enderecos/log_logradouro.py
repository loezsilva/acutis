from dataclasses import dataclass
from builder import db


@dataclass
class LogLogradouro(db.Model):
    __tablename__ = "log_logradouro"

    log_nu: int = db.Column(db.Integer, primary_key=True)
    ufe_sg: str = db.Column(db.String(2))
    loc_nu: int = db.Column(db.Integer)
    bai_nu_ini: int = db.Column(db.Integer)
    bai_nu_fim: int = db.Column(db.Integer)
    log_no: str = db.Column(db.String(100))
    log_complemento: str = db.Column(db.String(100))
    cep: str = db.Column(db.String(8))
    tlo_tx: str = db.Column(db.String(36))
    log_sta_tlo: str = db.Column(db.String(1))
    log_no_abrev: str = db.Column(db.String(36))

    def __repr__(self):
        return f"<LogLogradouro {self.log_nu}>"
