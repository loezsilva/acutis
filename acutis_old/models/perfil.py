from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel

from builder import db
from utils.functions import get_current_time


class ProfilesEnum(str, Enum):
    ADMINISTRADOR: str = "Administrador"
    BENFEITOR: str = "Benfeitor"
    OPERACIONAL: str = "Operacional"
    CAMPANHAS_E_LP: str = "Campanhas e LP"
    MARKETING: str = "Marketing"
    DEV: str = "Dev"
    ADMINISTRADOR_AGAPE: str = "Administrador Agape"
    VOLUNTARIO_AGAPE: str = "Voluntario Agape"
    GESTOR_DOACOES: str = "Gestor Doacoes"
    VOCACIONAL_MASCULINO: str = "Vocacional Masculino"
    VOCACIONAL_FEMININO: str = "Vocacional Feminino"


@dataclass
class Perfil(db.Model):
    __tablename__ = "perfil"

    id: int = db.Column(db.Integer, primary_key=True)
    fk_sistema_id: int = db.Column(db.Integer, db.ForeignKey("sistema.id"))
    nome: str = db.Column(db.String(45), nullable=False)
    status: bool = db.Column(db.Boolean, default=False)
    super_perfil: bool = db.Column(db.Boolean)
    data_criacao: datetime = db.Column(db.DateTime, default=get_current_time)
    usuario_criacao: int = db.Column(db.Integer, nullable=False)
    data_alteracao: datetime = db.Column(db.DateTime)
    usuario_alteracao: int = db.Column(db.Integer)

    permissoes_usuarios = db.relationship(
        "PermissaoUsuario", backref="profile", lazy="dynamic"
    )

    permissao_menu = db.relationship(
        "PermissaoMenu", backref="profile", cascade="all, delete"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "fk_sistema_id": self.fk_sistema_id,
            "nome": self.nome,
            "status": self.status,
            "data_criacao": self.data_criacao,
            "usuario_criacao": self.usuario_criacao,
            "data_alteracao": self.data_alteracao,
            "usuario_alteracao": self.usuario_alteracao,
        }

    def __repr__(self) -> str:
        return f"<Perfil: {self.nome}>"


class PermissionsMenuProfileSchema(BaseModel):
    menu_id: int
    acessar: bool
    criar: bool
    editar: bool
    deletar: bool


class ProfileCreateSchema(BaseModel):
    fk_sistema_id: Optional[int]
    nome: str
    status: bool
    super_perfil: bool


class ProfileUpdateSchema(ProfileCreateSchema):
    menus: List[PermissionsMenuProfileSchema]


class ProfileResponseSchema(BaseModel):
    id: int
    nome: str
    status: bool
    super_perfil: bool
    data_criacao: str | datetime

    class Config:
        orm_mode = True


class GetAllProfilesSchema(ProfileResponseSchema):
    quantidade_usuarios: int


class ProfileResponseListSchema(BaseModel):
    __root__: List[GetAllProfilesSchema]


class ProfileMenuGetByIdSchema(PermissionsMenuProfileSchema):
    nome_menu: str


class ProfileWithPermissionsResponseSchema(ProfileResponseSchema):
    menus: List[ProfileMenuGetByIdSchema]
