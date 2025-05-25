from datetime import datetime

from pydantic import BaseModel

from builder import db


class LandPageContent(db.Model):
    __tablename__ = "conteudo_landpage"

    id = db.Column(db.Integer, primary_key=True)
    landpage_id = db.Column(
        db.Integer, db.ForeignKey("landpage.id"), nullable=False
    )
    imagem = db.Column(db.String(100), nullable=False)
    html = db.Column(db.UnicodeText, nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    usuario_criacao = db.Column(db.Integer, nullable=False)
    data_alteracao = db.Column(db.DateTime)
    usuario_alteracao = db.Column(db.Integer)


class LandPageContentCreateSchema(BaseModel):
    id: int = None
    imagem: str
    html: str


class LandPageContentResponseSchema(BaseModel):
    id: int
    landpage_id: int
    imagem: str
    html: str
    data_criacao: datetime
    usuario_criacao: int
    data_alteracao: datetime = None
    usuario_alteracao: int = None

    class Config:
        orm_mode = True
