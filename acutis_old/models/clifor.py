from dataclasses import dataclass
from datetime import datetime, date

from builder import db
from utils.functions import get_current_time


@dataclass
class Clifor(db.Model):
    __tablename__ = "clifor"

    id: int = db.Column(db.Integer, primary_key=True)
    fk_empresa_id: int = db.Column(db.Integer, db.ForeignKey("empresa.id"))
    fk_municipio_id: int = db.Column(db.Integer, db.ForeignKey("municipio.id"))
    fk_tipo_clifor_id: int = db.Column(
        db.Integer, db.ForeignKey("tipo_clifor.id")
    )
    fk_usuario_id: int = db.Column(
        db.Integer, db.ForeignKey("usuario.id"), index=True
    )
    tipo_clifor: str = db.Column(db.String(1))
    nome_fantasia: str = db.Column(db.String(100))
    nome: str = db.Column(db.String(100), index=True)
    pf_pj: str = db.Column(db.String(1))
    cpf_cnpj: str = db.Column(db.String(20), index=True)
    telefone1: str = db.Column(db.String(30))
    telefone2: str = db.Column(db.String(15))
    email: str = db.Column(db.String(60), index=True)
    status: int = db.Column(db.Integer, index=True)
    data_nascimento: date = db.Column(db.Date)
    sexo: str = db.Column(db.String(20))
    data_criacao: datetime = db.Column(db.DateTime, default=get_current_time)
    usuario_criacao: int = db.Column(db.Integer, nullable=False, default=0)
    data_alteracao: datetime = db.Column(db.DateTime)
    usuario_alteracao: int = db.Column(db.Integer)

    endereços = db.relationship(
        "Endereco", backref="clifor", lazy="dynamic", cascade="all, delete"
    )

    def __repr__(self) -> str:
        return f"<Clifor: {self.id}>"
