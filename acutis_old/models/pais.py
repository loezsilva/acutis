from datetime import datetime
from typing import List

from pydantic import BaseModel

from builder import db


class Pais(db.Model):
    __tablename__ = "pais"

    id = db.Column(db.Integer, primary_key=True)
    cod_pais = db.Column(db.String(5), nullable=False)
    nome = db.Column(db.String(60), nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    usuario_criacao = db.Column(db.Integer, nullable=False)
    data_alteracao = db.Column(db.DateTime)
    usuario_alteracao = db.Column(db.Integer)

    estados = db.relationship("Estado", backref="country", lazy="dynamic")

    def to_dict(self):
        return {
            "id": self.id,
            "cod_pais": self.cod_pais,
            "nome": self.nome,
            "data_criacao": self.data_criacao,
            "usuario_criacao": self.usuario_criacao,
            "data_alteracao": self.data_alteracao,
            "usuario_alteracao": self.usuario_alteracao,
        }

    def __repr__(self) -> str:
        return f"<Pais {self.nome}>"


class CountryCreateSchema(BaseModel):
    cod_pais: str
    nome: str


class CountryResponseSchema(BaseModel):
    id: int
    cod_pais: str
    nome: str
    data_criacao: datetime
    usuario_criacao: int
    data_alteracao: datetime = None
    usuario_alteracao: int = None

    class Config:
        orm_mode = True


class CountryResponseListSchema(BaseModel):
    __root__: List[CountryResponseSchema]
