from dataclasses import dataclass
from datetime import datetime, date
from typing import List, Optional

from pydantic import BaseModel, constr

from builder import db
from models.conteudo_landpage import LandPageContentCreateSchema
from utils.functions import get_current_time


@dataclass
class Campanha(db.Model):
    __tablename__ = "campanha"

    id: int = db.Column(db.Integer, primary_key=True)
    fk_empresa_id: int = db.Column(db.Integer, db.ForeignKey("empresa.id"))
    titulo: str = db.Column(db.String(50), nullable=False)
    descricao: str = db.Column(db.UnicodeText)
    data_inicio: date = db.Column(db.Date)
    data_fim: date = db.Column(db.Date)
    valor_meta: float = db.Column(db.Numeric(15, 4))
    prorrogado: int = db.Column(db.Integer)
    data_prorrogacao: date = db.Column(db.Date)
    valor_total_atingido: float = db.Column(db.Numeric(15, 4))
    data_fechamento_campanha: date = db.Column(db.Date)
    status: bool = db.Column(db.Boolean, nullable=False)
    publica: bool = db.Column(db.Boolean, nullable=False)
    filename: str = db.Column(db.String)
    chave_pix: str = db.Column(db.String(100))
    data_criacao: datetime = db.Column(db.DateTime, default=get_current_time)
    usuario_criacao: int = db.Column(db.Integer, nullable=False)
    data_alteracao: datetime = db.Column(db.DateTime)
    usuario_alteracao: int = db.Column(db.Integer)
    duracao: str = db.Column(db.String(11), nullable=True)
    deleted_at: datetime = db.Column(db.DateTime)
    objetivo: str = db.Column(db.String)
    cadastros_meta: int = db.Column(db.Integer)
    preenchimento_foto: bool = db.Column(db.Boolean, default=False)
    label_foto: str = db.Column(db.String(100))
    zone: str = db.Column(db.String(100))
    zone_id: str = db.Column(db.String(40))
    contabilizar_doacoes: bool = db.Column(db.Boolean, default=True)

    historico_doacoes = db.relationship(
        "HistoricoCampanhaDonations",
        cascade="all, delete",
        backref="campanha_historico",
        overlaps="campanha_historico,historico_doacoes",
    )

    pedido = db.relationship(
        "Pedido", backref="campaign", lazy="dynamic", cascade="all, delete"
    )

    landpage = db.relationship(
        "LandPage", backref="campaign", lazy="dynamic", cascade="all, delete"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "fk_empresa_id": self.fk_empresa_id,
            "titulo": self.titulo,
            "descricao": self.descricao,
            "data_inicio": self.data_inicio,
            "data_fim": self.data_fim,
            "valor_meta": self.valor_meta,
            "prorrogado": self.prorrogado,
            "data_prorrogacao": self.data_prorrogacao,
            "valor_total_atingido": self.valor_total_atingido,
            "data_fechamento_campanha": self.data_fechamento_campanha,
            "status": self.status,
            "filename": self.filename,
            "data_criacao": self.data_criacao,
            "usuario_criacao": self.usuario_criacao,
            "data_alteracao": self.data_alteracao,
            "usuario_alteracao": self.usuario_alteracao,
            "publica": self.publica,
            "duracao": self.duracao,
            "deleted_at": self.deleted_at,
            "objetivo": self.objetivo,
            "cadastros_meta": self.cadastros_meta,
        }

    def soft_delete(self):
        self.deleted_at = get_current_time()
        db.session.commit()

    def __repr__(self) -> str:
        return (
            f"<Campanha id:{self.id}, "
            f"valor_meta:{self.valor_meta}, "
            f"valor_total_atingido:{self.valor_total_atingido}, "
            f"duracao:{self.duracao}>"
        )


class CampaignCreateSchema(BaseModel):
    titulo: constr(max_length=50)  # type: ignore
    descricao: str = None
    data_inicio: Optional[date]
    data_fim: Optional[date]
    valor_meta: float = None
    prorrogado: int = None
    data_prorrogacao: date = None
    valor_total_atingido: float = None
    data_fechamento_campanha: date = None
    status: bool
    imagem_capa: str
    chave_pix: Optional[str]
    credito_unico: Optional[int]
    credito_recorrente: Optional[int]
    pix_unico: Optional[int]
    pix_recorrente: Optional[int]
    boleto_unico: Optional[int]
    boleto_recorrente: Optional[int]
    publica: int
    duracao: str
    objetivo: str
    cadastros_meta: Optional[int]
    preenchimento_foto: Optional[bool]
    label_foto: Optional[str]
    background: Optional[str]
    banner: Optional[str]
    tipo_cadastro: Optional[str]
    url: Optional[str]
    conteudo: Optional[List[LandPageContentCreateSchema]]
    cadastrar_landing_page: Optional[bool]
    texto_pos_registo: Optional[str]
    texto_email_pos_registro: Optional[str]


class CampaignQuerySchema(BaseModel):
    ativo: bool = False


class CampaignResponseSchema(BaseModel):
    id: int
    fk_empresa_id: int
    titulo: str
    descricao: str = None
    data_inicio: date = None
    data_fim: date = None
    valor_meta: float = None
    prorrogado: int = None
    data_prorrogacao: date = None
    valor_total_atingido: float = None
    data_fechamento_campanha: date = None
    status: int
    filename: str = None
    chave_pix: Optional[str]
    data_criacao: datetime
    usuario_criacao: int
    data_alteracao: datetime = None
    usuario_alteracao: int = None
    publica: int
    duracao: Optional[str]
    objetivo: str
    cadastros_meta: int = None
    cadastros_total_atingido: Optional[int]
    preenchimento_foto: Optional[int]
    label_foto: Optional[str]

    class Config:
        orm_mode = True


class CampaignResponseListSchema(BaseModel):
    __root__: List[CampaignResponseSchema]


class UserSchema(BaseModel):
    id: int
    nome: str
    email: str
    data_cadastro: str
    ultimo_acesso: Optional[str]
    status: bool


class DonationSchema(BaseModel):
    id: int
    valor: float
    data_doacao: str
    recorrente: bool
    transaction_id: str
    referencia: str
    clifor: str
    forma_pagamento: int
    status_pedido: int


class PaginationSchema(BaseModel):
    current_page: int
    total_pages: int
    per_page: int
    total_items: int


class CountCampaignQuerySchema(BaseModel):
    donations: List[DonationSchema]
    users: List[UserSchema]
    campaign: str
    total_donations: float
    total_users: int
    pagination_users: PaginationSchema
    pagination_donations: PaginationSchema
