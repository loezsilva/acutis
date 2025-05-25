from dataclasses import dataclass
from datetime import datetime
from exceptions.errors_handler import errors_handler
from builder import db
from utils.functions import get_current_time


@dataclass
class Generais(db.Model):
    __tablename__ = "generais"

    id: int = db.Column(db.Integer, primary_key=True)
    fk_usuario_id: int = db.Column(
        db.Integer, db.ForeignKey("usuario.id"), index=True, unique=True
    )
    quant_membros_grupo: int = db.Column(db.Integer)
    created_at: datetime = db.Column(db.DateTime, default=get_current_time)
    deleted_at: datetime = db.Column(db.DateTime)
    updated_at: datetime = db.Column(db.DateTime)
    usuario_alteracao: int = db.Column(db.Integer)
    fk_usuario_superior_id: int = db.Column(db.Integer)
    fk_cargo_id: int = db.Column(
        db.Integer, db.ForeignKey("cargo.id"), index=True
    )
    link_grupo: str = db.Column(db.String)
    nome_grupo: str = db.Column(db.String)
    tempo_de_administrador: int = db.Column(db.Integer, default=0)
    status: bool = db.Column(db.Boolean, default=False)

    def soft_delete(self):
        try:
            self.deleted_at = get_current_time()
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return errors_handler(e)
