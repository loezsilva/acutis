from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from builder import db
from utils.functions import get_current_time


class VocationalGendersEnum(str, Enum):
    MASCULINO = "masculino"
    FEMININO = "feminino"


@dataclass
class UsuarioVocacional(db.Model):
    __tablename__ = "usuarios_vocacional"

    id: int = db.Column(db.Integer, primary_key=True)
    nome: int = db.Column(db.String(100), nullable=False)
    email: str = db.Column(db.String(120), nullable=False, unique=True)
    telefone: str = db.Column(db.String(30), nullable=False)
    genero: VocationalGendersEnum = db.Column(
        db.String(10), nullable=False, index=True
    )
    pais: str = db.Column(db.String(100), nullable=False)
    created_at: datetime = db.Column(db.DateTime, default=get_current_time)
    updated_at: datetime = db.Column(db.DateTime)

    etapas = db.relationship('EtapaVocacional', backref='usuario_vocacional', cascade='all, delete')
    fichas = db.relationship('FichaVocacional', backref='usuario_vocacional', cascade='all, delete')
    cadastros = db.relationship('CadastroVocacional', backref='usuario_vocacional', cascade='all, delete')