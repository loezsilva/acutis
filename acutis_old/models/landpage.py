from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from builder import db
from models.conteudo_landpage import (
    LandPageContentCreateSchema,
    LandPageContentResponseSchema,
)


class LandPage(db.Model):
    __tablename__ = "landpage"

    id = db.Column(db.Integer, primary_key=True)
    campanha_id = db.Column(
        db.Integer, db.ForeignKey("campanha.id"), index=True
    )
    background = db.Column(db.String(100), nullable=True)
    banner = db.Column(db.String(100), nullable=False)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.UnicodeText, nullable=False)
    tipo_cadastro = db.Column(db.String(50), nullable=False)
    url = db.Column(db.String, nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    usuario_criacao = db.Column(db.Integer, nullable=False)
    data_alteracao = db.Column(db.DateTime)
    usuario_alteracao = db.Column(db.Integer)
    type = db.Column(db.Integer, default=1)
    texto_pos_registro = db.Column(db.UnicodeText, default="", nullable=False)
    texto_email_pos_registro = db.Column(
        db.UnicodeText, default="", nullable=False
    )
    deleted_at = db.Column(db.DateTime)

    conteudo_landpage = db.relationship(
        "LandPageContent",
        backref="landpage",
        lazy="dynamic",
        cascade="all, delete",
    )

    def soft_delete(self):
        self.deleted_at = datetime.now()
        db.session.commit()

    def restore(self):
        self.deleted_at = None
        db.session.commit()

    def to_dict(self):
        not_return = [
            "data_criacao",
            "usuario_criacao",
            "data_alteracao",
            "usuario_alteracao",
        ]
        return {
            c.name: getattr(self, c.name)
            for c in self.__table__.columns
            if c.name not in not_return
        }

    def __repr__(self) -> str:
        return f"<LandPage: {self.id}>"


class LandPageCreateSchema(BaseModel):
    titulo: str
    descricao: str
    campanha_id: int = None
    background: str
    banner: str
    tipo_cadastro: str
    url: str
    conteudo: List[LandPageContentCreateSchema]


class LandPageResponseSchema(BaseModel):
    id: int
    campanha_id: int = None
    background: Optional[str]
    banner: str
    titulo: str
    descricao: str
    tipo_cadastro: str
    url: str
    data_criacao: datetime
    usuario_criacao: int
    data_alteracao: datetime = None
    usuario_alteracao: int = None
    texto_pos_registro: str
    texto_email_pos_registro: str
    preenchimento_foto: Optional[bool]
    label_foto: Optional[str]
    objetivo: Optional[str]

    class Config:
        orm_mode = True


class LandPageWithContentResponseSchema(LandPageResponseSchema):
    conteudo: List[LandPageContentResponseSchema]


class LandPageResponseListSchema(BaseModel):
    __root__: List[LandPageResponseSchema]
