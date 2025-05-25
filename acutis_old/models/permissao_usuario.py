from dataclasses import dataclass
from datetime import datetime


from builder import db
from utils.functions import get_current_time


@dataclass
class PermissaoUsuario(db.Model):
    __tablename__ = "permissao_usuario"

    id: int = db.Column(db.Integer, primary_key=True)
    fk_empresa_id = db.Column(db.Integer, db.ForeignKey("empresa.id"))
    fk_usuario_id: int = db.Column(
        db.Integer, db.ForeignKey("usuario.id"), index=True
    )
    fk_sistema_id = db.Column(db.Integer, db.ForeignKey("sistema.id"))
    fk_perfil_id: int = db.Column(
        db.Integer, db.ForeignKey("perfil.id"), index=True
    )
    data_criacao: datetime = db.Column(db.DateTime, default=get_current_time)
    usuario_criacao: int = db.Column(db.Integer, nullable=False)
    data_alteracao: datetime = db.Column(db.DateTime)
    usuario_alteracao: int = db.Column(db.Integer)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self) -> str:
        return f"<PermissaoUsuario: {self.id}>"
