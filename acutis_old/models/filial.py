from datetime import date, datetime
from typing import List

from pydantic import BaseModel, constr

from builder import db


class Filial(db.Model):
    __tablename__ = "filial"

    id = db.Column(db.Integer, primary_key=True)
    fk_empresa_id = db.Column(
        db.Integer, db.ForeignKey("empresa.id"), nullable=False
    )
    fk_municipio_id = db.Column(
        db.Integer, db.ForeignKey("municipio.id"), nullable=False
    )
    nome_fantasia = db.Column(db.String(255))
    razao_social = db.Column(db.String(255))
    cnpj = db.Column(db.String(20), nullable=False, unique=True)
    inscricao_estadual = db.Column(db.String(20))
    inscricao_municipal = db.Column(db.String(20))
    num_reg_junta = db.Column(db.String(20))
    data_reg_junta = db.Column(db.Date)
    cod_atividade_principal = db.Column(db.String(20))
    desc_atividade_principal = db.Column(db.String(200))
    telefone1 = db.Column(db.String(15))
    telefone2 = db.Column(db.String(15))
    email = db.Column(db.String(60), unique=True, nullable=False)
    rua = db.Column(db.String(100))
    numero = db.Column(db.String(8))
    complemento = db.Column(db.String(60))
    bairro = db.Column(db.String(80))
    cep = db.Column(db.String(9))
    status = db.Column(db.Boolean, default=True)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    usuario_criacao = db.Column(db.Integer, nullable=False)
    data_alteracao = db.Column(db.DateTime)
    usuario_alteracao = db.Column(db.Integer)

    def to_dict(self):
        return {
            "id": self.id,
            "fk_empresa_id": self.fk_empresa_id,
            "fk_municipio_id": self.fk_municipio_id,
            "nome_fantasia": self.nome_fantasia,
            "razao_social": self.razao_social,
            "cnpj": self.cnpj,
            "inscricao_estadual": self.inscricao_estadual,
            "inscricao_municipal": self.inscricao_municipal,
            "num_reg_junta": self.num_reg_junta,
            "data_reg_junta": self.data_reg_junta,
            "cod_atividade_principal": self.cod_atividade_princ,
            "desc_atividade_principal": self.desc_atividade_princ,
            "telefone1": self.telefone1,
            "telefone2": self.telefone2,
            "email": self.email,
            "rua": self.rua,
            "numero": self.numero,
            "complemento": self.complemento,
            "bairro": self.bairro,
            "cep": self.cep,
            "status": self.status,
            "data_criacao": self.data_criacao,
            "usuario_criacao": self.usuario_criacao,
            "data_alteracao": self.data_alteracao,
            "usuario_alteracao": self.usuario_alteracao,
        }

    def __repr__(self) -> str:
        return f"<Filial {self.nome_fantasia}>"


class BranchCreateSchema(BaseModel):
    fk_empresa_id: int
    fk_municipio_id: int
    nome_fantasia: str = None
    razao_social: str = None
    cnpj: constr(min_length=14, max_length=14)
    inscricao_estadual: str = None
    inscricao_municipal: str = None
    num_reg_junta: str = None
    data_reg_junta: date = None
    cod_atividade_principal: str = None
    desc_atividade_principal: str = None
    telefone1: str = None
    telefone2: str = None
    email: str
    rua: str = None
    numero: str = None
    complemento: str = None
    bairro: str = None
    cep: constr(min_length=8, max_length=8) = None
    status: bool = True


class BranchResponseSchema(BaseModel):
    id: int
    fk_empresa_id: int
    fk_municipio_id: int
    nome_fantasia: str = None
    razao_social: str = None
    cnpj: str
    inscricao_estadual: str = None
    inscricao_municipal: str = None
    num_reg_junta: str = None
    data_reg_junta: date = None
    cod_atividade_principal: str = None
    desc_atividade_principal: str = None
    telefone1: str = None
    telefone2: str = None
    email: str
    rua: str = None
    numero: str = None
    complemento: str = None
    bairro: str = None
    cep: str = None
    status: bool
    data_criacao: datetime
    usuario_criacao: int
    data_alteracao: datetime = None
    usuario_alteracao: int = None

    class Config:
        orm_mode = True


class BranchResponseListSchema(BaseModel):
    __root__: List[BranchResponseSchema]
