from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from builder import db
from utils.functions import get_current_time


@dataclass
class MenuSistema(db.Model):
    __tablename__ = "menu_sistema"

    id: int = db.Column(db.Integer, primary_key=True)
    fk_sistema_id: int = db.Column(db.Integer, db.ForeignKey("sistema.id"))
    slug: str = db.Column(db.String(50), nullable=False, unique=True)
    menu: str = db.Column(db.String(255), nullable=False)
    data_criacao: datetime = db.Column(db.DateTime, default=get_current_time)
    usuario_criacao: int = db.Column(db.Integer, nullable=False)
    data_alteracao: datetime = db.Column(db.DateTime)
    usuario_alteracao: int = db.Column(db.Integer)

    permissoes = db.relationship(
        "PermissaoMenu",
        backref="MenuSistema",
        lazy="dynamic",
        cascade="all, delete",
    )

    def to_dict(self):
        return {
            "id": self.id,
            "fk_sistema_id": self.fk_sistema_id,
            "slug": self.slug,
            "menu": self.menu,
            "data_criacao": self.data_criacao,
            "usuario_criacao": self.usuario_criacao,
            "data_alteracao": self.data_alteracao,
            "usuario_alteracao": self.usuario_alteracao,
        }

    def __repr__(self) -> str:
        return f"MenuSistema: {self.menu}"


class SystemMenuCreateSchema(BaseModel):
    fk_sistema_id: int
    slug: str
    menu: str


class SystemMenuResponseSchema(BaseModel):
    id: int
    fk_sistema_id: int
    slug: str
    menu: str
    data_criacao: datetime
    usuario_criacao: int
    data_alteracao: datetime = None
    usuario_alteracao: int = None

    class Config:
        orm_mode = True


class SystemMenuResponseListSchema(BaseModel):
    __root__: List[SystemMenuResponseSchema]


class FilterSystemMenuBySystemIdSchema(BaseModel):
    sistema_id: Optional[int] = None
