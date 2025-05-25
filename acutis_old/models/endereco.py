from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional

from pydantic import BaseModel

from builder import db
from utils.functions import get_current_time


@dataclass
class Endereco(db.Model):
    __tablename__ = "endereco"

    id: int = db.Column(db.Integer, primary_key=True)
    fk_clifor_id: int = db.Column(
        db.Integer, db.ForeignKey("clifor.id"), nullable=True, index=True
    )
    rua: str = db.Column(db.String(100))
    numero: str = db.Column(db.String(8))
    complemento: str = db.Column(db.String(60))
    ponto_referencia: str = db.Column(db.String(100))
    bairro: str = db.Column(db.String(80))
    cidade: str = db.Column(db.String(32))
    estado: str = db.Column(db.String(80))
    cep: str = db.Column(db.String(9), index=True)
    obriga_atualizar_endereco: bool = db.Column(db.Boolean, default=False)
    ultima_atualizacao_endereco: date = db.Column(db.Date)
    data_criacao: datetime = db.Column(db.DateTime, default=get_current_time)
    usuario_criacao: int = db.Column(db.Integer, nullable=False, default=0)
    data_alteracao: datetime = db.Column(db.DateTime)
    usuario_alteracao: int = db.Column(db.Integer)
    detalhe_estrangeiro: str = db.Column(db.Text)
    pais_origem: str = db.Column(db.Text, default="brasil")
    latitude: float = db.Column(db.Float)
    longitude: float = db.Column(db.Float)
    latitude_nordeste: float = db.Column(db.Float)
    longitude_nordeste: float = db.Column(db.Float)
    latitude_sudoeste: float = db.Column(db.Float)
    longitude_sudoeste: float = db.Column(db.Float)

    def __repr__(self) -> str:
        return f"<Endereço: {self.id}>"


class AddressCreateSchema(BaseModel):
    rua: str = None
    numero: str = None
    complemento: str = None
    bairro: str = None
    cidade: str = None
    cep: str = None


class AddressResponseSchema(BaseModel):
    id: int
    fk_clifor_id: int
    rua: str = None
    numero: str = None
    complemento: str = None
    bairro: str = None
    cidade: str = None
    cep: str = None
    obriga_atualizar_endereco: bool
    ultima_atualizacao_endereco: date = None
    data_criacao: datetime
    usuario_criacao: int
    data_alteracao: datetime = None
    usuario_alteracao: int = None
    estado: Optional[str]
    detalhe_estrangeiro: str = None

    class Config:
        orm_mode = True

class AtualizarEnderecoPorUserIdResponse(BaseModel):
    msg: str