from dataclasses import dataclass
from datetime import datetime

from builder import db
from utils.functions import get_current_time


@dataclass
class PermissaoMenu(db.Model):
    __tablename__ = "permissao_menu"

    id: int = db.Column(db.Integer, primary_key=True)
    fk_perfil_id: int = db.Column(db.Integer, db.ForeignKey("perfil.id"))
    fk_menu_id: int = db.Column(db.Integer, db.ForeignKey("menu_sistema.id"))
    acessar: int = db.Column(db.SmallInteger)
    criar: int = db.Column(db.SmallInteger)
    editar: int = db.Column(db.SmallInteger)
    deletar: int = db.Column(db.SmallInteger)
    data_criacao: datetime = db.Column(db.DateTime, default=get_current_time)
    usuario_criacao: int = db.Column(db.Integer, nullable=False)
    data_alteracao: datetime = db.Column(db.DateTime)
    usuario_alteracao: int = db.Column(db.Integer)

    def to_dict(self):
        return {
            "id": self.id,
            "fk_perfil_id": self.fk_perfil_id,
            "fk_menu_id": self.fk_menu_id,
            "acessar": self.acessar,
            "criar": self.criar,
            "editar": self.editar,
            "deletar": self.deletar,
            "data_criacao": self.data_criacao,
            "usuario_criacao": self.usuario_criacao,
            "data_alteracao": self.data_alteracao,
            "usuario_alteracao": self.usuario_alteracao,
        }

    def __repr__(self) -> str:
        return f"PermissaoMenu: {self.id}"
