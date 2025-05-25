from datetime import datetime

from pydantic import BaseModel, constr
from typing import List

from builder import db


class Empresa(db.Model):
    __tablename__ = "empresa"

    id = db.Column(db.Integer, primary_key=True)
    fk_municipio_id = db.Column(
        db.Integer, db.ForeignKey("municipio.id"), nullable=False
    )
    nome_fantasia = db.Column(db.String(255), nullable=False)
    razao_social = db.Column(db.String(255), nullable=False)
    cnpj = db.Column(db.String(20), nullable=False, unique=True)
    inscricao_estadual = db.Column(db.String(20))
    telefone1 = db.Column(db.String(15), nullable=False)
    telefone2 = db.Column(db.String(15))
    email = db.Column(db.String(60), unique=True)
    rua = db.Column(db.String(100))
    numero = db.Column(db.String(8))
    complemento = db.Column(db.String(60))
    bairro = db.Column(db.String(80))
    pais = db.Column(db.String(20))
    cep = db.Column(db.String(9))
    status = db.Column(db.Boolean, default=True)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    usuario_criacao = db.Column(db.Integer, nullable=False)
    data_alteracao = db.Column(db.DateTime)
    usuario_alteracao = db.Column(db.Integer)

    filiais = db.relationship(
        "Filial", backref="company", lazy="dynamic", cascade="all, delete"
    )
    campanhas = db.relationship("Campanha", backref="company", lazy="dynamic")
    permissoes_usuarios = db.relationship(
        "PermissaoUsuario", backref="company", lazy="dynamic"
    )
    gateway_pagamento = db.relationship(
        "GatewayPagamento",
        backref="company",
        lazy="dynamic",
        cascade="all, delete",
    )

    def to_dict(self):
        return {
            "id": self.id,
            "fk_municipio_id": self.fk_municipio_id,
            "nome_fantasia": self.nome_fantasia,
            "razao_social": self.razao_social,
            "cnpj": self.cnpj,
            "inscricao_estadual": self.inscricao_estadual,
            "telefone1": self.telefone1,
            "telefone2": self.telefone2,
            "email": self.email,
            "rua": self.rua,
            "numero": self.numero,
            "complemento": self.complemento,
            "bairro": self.bairro,
            "pais": self,
            "cep": self.cep,
            "status": self.status,
            "data_criacao": self.data_criacao,
            "usuario_criacao": self.usuario_criacao,
            "data_alteracao": self.data_alteracao,
        }

    def __repr__(self) -> str:
        return f"<Empresa {self.nome_fantasia}>"


class CompanyCreateSchema(BaseModel):
    fk_municipio_id: int
    nome_fantasia: str
    razao_social: str
    cnpj: constr(min_length=14, max_length=14)
    inscricao_estadual: str = None
    telefone1: str
    telefone2: str = None
    email: str
    rua: str = None
    numero: str = None
    complemento: str = None
    bairro: str = None
    cep: str = None
    status: bool = True


class CompanyResponseSchema(BaseModel):
    id: int
    fk_municipio_id: int
    nome_fantasia: str
    razao_social: str
    cnpj: str
    inscricao_estadual: str = None
    telefone1: str
    telefone2: str = None
    email: str
    rua: str = None
    numero: str = None
    complemento: str = None
    bairro: str = None
    pais: str = None
    cep: str = None
    status: bool
    data_criacao: datetime
    usuario_criacao: int
    data_alteracao: datetime = None
    usuario_alteracao: int = None

    class Config:
        orm_mode = True


class CompanyResponseListSchema(BaseModel):
    __root__: List[CompanyResponseSchema]
