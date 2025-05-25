from datetime import datetime
from typing import List

from pydantic import BaseModel, constr

from builder import db


class Sistema(db.Model):
    __tablename__ = "sistema"

    id = db.Column(db.Integer, primary_key=True)
    nome_sistema = db.Column(db.String(20), nullable=False)
    descricao = db.Column(db.String(200), nullable=False)
    versao = db.Column(db.String(15), nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    usuario_criacao = db.Column(db.Integer, nullable=False)
    data_alteracao = db.Column(db.DateTime)
    usuario_alteracao = db.Column(db.Integer)

    perfis = db.relationship("Perfil", backref="system", lazy="dynamic")
    permissoes_usuarios = db.relationship(
        "PermissaoUsuario", backref="system", lazy="dynamic"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "nome_sistema": self.nome_sistema,
            "descricao": self.descricao,
            "versao": self.versao,
            "data_criacao": self.data_criacao,
            "usuario_criacao": self.usuario_criacao,
            "data_alteracao": self.data_alteracao,
            "usuario_alteracao": self.usuario_alteracao,
        }

    def __repr__(self) -> str:
        return f"<Sistema {self.nome_sistema}>"


class SystemCreateSchema(BaseModel):
    nome_sistema: constr(max_length=20)
    descricao: str
    versao: constr(max_length=15)


class SystemResponseSchema(BaseModel):
    id: int
    nome_sistema: str
    descricao: str
    versao: str
    data_criacao: datetime
    usuario_criacao: int
    data_alteracao: datetime = None
    usuario_alteracao: int = None

    class Config:
        orm_mode = True


class SystemResponseListSchema(BaseModel):
    __root__: List[SystemResponseSchema]
