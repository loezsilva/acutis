from dataclasses import dataclass
from datetime import datetime
from builder import db
from pydantic import BaseModel
from typing import Dict, List, Optional

from utils.functions import get_current_time


@dataclass
class EventoUsuario(db.Model):
    __tablename__ = "evento_usuario"

    id: int = db.Column(db.Integer, primary_key=True)
    fk_usuario_id: int = db.Column(
        db.Integer, db.ForeignKey("usuario.id"), nullable=False
    )
    fk_campanha_id: int = db.Column(
        db.Integer, db.ForeignKey("campanha.id"), nullable=True
    )
    fk_landpage_id: int = db.Column(
        db.Integer, db.ForeignKey("landpage.id"), nullable=True
    )
    presencas: int = db.Column(db.Integer, nullable=False)
    data_register: datetime = db.Column(
        db.DateTime, nullable=False, default=get_current_time
    )

    usuario = db.relationship("Usuario", backref="usuario")
    campanha = db.relationship("Campanha", backref="campanha")
    landpage = db.relationship("LandPage", backref="campanha")

    def __repr__(self) -> str:
        return f"<EventoUsuario: (id={self.id}, fk_usuario_id={self.fk_usuario_id}, fk_landpage_id={self.fk_landpage_id}, fk_campanha_id={self.fk_campanha_id}, presenca={self.presenca})>"

    def to_dict(self) -> Dict:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class EventoUsuarioSchema(BaseModel):
    user_id: int
    campanha_id: Optional[int]


class Eventousuario(BaseModel):
    benfeitor: str
    campaign_id: int
    campaign_name: str
    cpf_cnpj: str
    email: str
    id_user: int
    presencas: int


class EventoUsuarioResponseSchema(BaseModel):
    presences: List[Eventousuario]


class ResponseFrequencias(BaseModel):
    campanhas: int
    frequencias: int
