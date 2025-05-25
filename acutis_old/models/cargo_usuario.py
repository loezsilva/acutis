from datetime import datetime
from typing import List

from pydantic import BaseModel

from builder import db


class CargoUsuario(db.Model):
    __tablename__ = "cargo_usuario"

    id = db.Column(db.Integer, primary_key=True)
    fk_usuario_id = db.Column(
        db.Integer, db.ForeignKey("usuario.id"), nullable=False
    )
    fk_cargo_id = db.Column(
        db.Integer, db.ForeignKey("cargo.id"), nullable=False
    )
    fk_usuario_superior_id = db.Column(db.Integer, db.ForeignKey("usuario.id"))
    convite = db.Column(db.SmallInteger)
    data_convite_aceito = db.Column(db.DateTime)
    usuario_convite_aceito = db.Column(db.Integer)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    usuario_criacao = db.Column(db.Integer)
    data_alteracao = db.Column(db.DateTime)
    usuario_alteracao = db.Column(db.Integer)
    quant_membros_grupo = db.Column(db.Integer)
    tempo_de_membro = db.Column(db.Integer)
    print_grupo = db.Column(db.String)


class UserMarshalQuerySchema(BaseModel):
    aceitos: bool = False


class UserMarshalResponseSchema(BaseModel):
    nome: str
    id: int


class UserMarshalResponseListSchema(BaseModel):
    __root__: List[UserMarshalResponseSchema]


class MarshalGeneralQuerySchema(BaseModel):
    cargo_id: int = None
    superior_id: int = None


class MarshalGeneralResponseSchema(BaseModel):
    id: int
    nome: str
    convite: str
    cargo_id: int
    cargo: str
    superior_id: int = None
    data_modificacao: str = None
    nome_superior: str = None


class MarshalGeneralResponseListSchema(BaseModel):
    __root__: List[MarshalGeneralResponseSchema]


class UpdateInviteSchema(BaseModel):
    status_convite: int
