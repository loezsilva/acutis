from datetime import datetime
from typing import List

from pydantic import BaseModel, constr

from builder import db


class Estado(db.Model):
    __tablename__ = "estado"

    id = db.Column(db.Integer, primary_key=True)
    fk_pais_id = db.Column(
        db.Integer, db.ForeignKey("pais.id"), nullable=False
    )
    cod = db.Column(db.String(5), nullable=False)
    nome = db.Column(db.String(40), nullable=False)
    nacional = db.Column(db.Boolean, nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    usuario_criacao = db.Column(db.Integer, nullable=False)
    data_alteracao = db.Column(db.DateTime)
    usuario_alteracao = db.Column(db.Integer)

    municipios = db.relationship("Municipio", backref="state", lazy="dynamic")

    def to_dict(self):
        return {
            "id": self.id,
            "fk_pais_id": self.fk_pais_id,
            "cod": self.cod,
            "nome": self.nome,
            "nacional": self.nacional,
            "data_criacao": self.data_criacao,
            "usuario_criacao": self.usuario_criacao,
            "data_alteracao": self.data_alteracao,
            "usuario_alteracao": self.usuario_alteracao,
        }

    def __repr__(self) -> str:
        return f"<Estado {self.nome}>"


class StateCreateSchema(BaseModel):
    fk_pais_id: int
    cod: constr(max_length=5)
    nome: str
    nacional: bool


class StateResponseSchema(BaseModel):
    id: int
    fk_pais_id: int
    cod: str
    nome: str
    nacional: bool
    data_criacao: datetime
    usuario_criacao: int
    data_alteracao: datetime = None
    usuario_alteracao: int = None

    class Config:
        orm_mode = True


class StateResponseListSchema(BaseModel):
    __root__: List[StateResponseSchema]


class StateByCountryResponseSchema(BaseModel):
    id: int
    nome: str

    class Config:
        orm_mode = True


class StateByCountryListResponseSchema(BaseModel):
    __root__: List[StateByCountryResponseSchema]
