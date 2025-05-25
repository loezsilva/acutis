from datetime import datetime
from typing import List

from pydantic import BaseModel

from builder import db


class Municipio(db.Model):
    __tablename__ = "municipio"

    id = db.Column(db.Integer, primary_key=True)
    fk_estado_id = db.Column(
        db.Integer, db.ForeignKey("estado.id"), nullable=False
    )
    nome_municipio = db.Column(db.String(40), nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    usuario_criacao = db.Column(db.Integer, nullable=False)
    data_alteracao = db.Column(db.DateTime)
    usuario_alteracao = db.Column(db.Integer)

    empresas = db.relationship("Empresa", backref="city", lazy="dynamic")
    filiais = db.relationship("Filial", backref="city", lazy="dynamic")

    def to_dict(self):
        return {
            "id": self.id,
            "fk_estado_id": self.fk_estado_id,
            "nome_municipio": self.nome_municipio,
            "data_criacao": self.data_criacao,
            "usuario_criacao": self.usuario_criacao,
            "data_alteracao": self.data_alteracao,
            "usuario_alteracao": self.usuario_alteracao,
        }

    def __repr__(self) -> str:
        return f"<Municipio {self.nome_municipio}>"


class CityCreateSchema(BaseModel):
    fk_estado_id: int
    nome_municipio: str


class CityResponseSchema(BaseModel):
    id: int
    fk_estado_id: int
    nome_municipio: str
    data_criacao: datetime
    usuario_criacao: int
    data_alteracao: datetime = None
    usuario_alteracao: int = None

    class Config:
        orm_mode = True


class CityResponseListSchema(BaseModel):
    __root__: List[CityResponseSchema]


class CityByStateResponseSchema(BaseModel):
    id: int
    nome_municipio: str

    class Config:
        orm_mode = True


class CityByStateListResponseSchema(BaseModel):
    __root__: List[CityByStateResponseSchema]
