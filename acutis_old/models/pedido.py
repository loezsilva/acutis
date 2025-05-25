from dataclasses import dataclass
from datetime import datetime

from builder import db
from typing import Dict, Union, List, Optional
from pydantic import BaseModel, Field

from utils.functions import get_current_time


@dataclass
class Pedido(db.Model):
    __tablename__ = "pedido"

    id: int = db.Column(db.Integer, primary_key=True)
    fk_empresa_id: int = db.Column(db.Integer, db.ForeignKey("empresa.id"))
    fk_filial_id: int = db.Column(db.Integer, db.ForeignKey("filial.id"))
    fk_clifor_id: int = db.Column(
        db.Integer, db.ForeignKey("clifor.id"), nullable=False, index=True
    )
    fk_campanha_id: int = db.Column(
        db.Integer, db.ForeignKey("campanha.id"), index=True
    )
    fk_forma_pagamento_id: int = db.Column(
        db.Integer,
        db.ForeignKey("forma_pagamento.id"),
        nullable=False,
        index=True,
    )
    data_pedido: datetime = db.Column(
        db.DateTime, default=get_current_time, index=True
    )
    periodicidade: int = db.Column(db.SmallInteger, nullable=False, index=True)
    status_pedido: int = db.Column(db.SmallInteger, index=True)
    valor_total_pedido: float = db.Column(db.Numeric(15, 4))
    order_id: str = db.Column(db.String(100))
    recorrencia_ativa: bool = db.Column(db.Boolean, index=True)
    cancelada_em: datetime = db.Column(db.DateTime)
    anonimo: bool = db.Column(db.Boolean, nullable=False, default=False)
    vencimento_cartao: str = db.Column(db.String(7))
    contabilizar_doacao: bool = db.Column(db.Boolean, default=True, index=True)
    fk_gateway_pagamento_id: int = db.Column(
        db.Integer, db.ForeignKey("gateway_pagamento.id"), index=True
    )
    data_criacao: datetime = db.Column(db.DateTime, default=get_current_time)
    usuario_criacao: int = db.Column(db.Integer, nullable=False)
    data_alteracao: datetime = db.Column(db.DateTime)
    usuario_alteracao: int = db.Column(db.Integer)
    cancelada_por: int = db.Column(db.Integer)

    processamento_pedido = db.relationship(
        "ProcessamentoPedido",
        backref="order",
        lazy="dynamic",
        cascade="all, delete",
    )
    item_pedido = db.relationship(
        "ItemPedido", backref="order", lazy="dynamic", cascade="all, delete"
    )


class DonationMonthlyData(BaseModel):
    crescimento_percentual: float = Field(...)
    total_doacoes: Union[float, int] = Field(...)


class DonationProgressResponse(BaseModel):
    donations_per_month: Dict[str, DonationMonthlyData] = Field(...)


class PaymentMethodPercentage(BaseModel):
    boleto_percentage: str
    credito_percentage: str
    pix_percentage: str


class TotalDonationsPerMethod(BaseModel):
    total_boleto: str
    total_credito: str
    total_pix: str


class CampaignData(BaseModel):
    titulo: str
    id: int


class DonationStatsResponse(BaseModel):
    campaigns: List[CampaignData]
    payment_methods_percentage: Optional[PaymentMethodPercentage]
    total_donations: Optional[str]
    total_donations_per_method: Optional[TotalDonationsPerMethod]


class PaymentMethod(BaseModel):
    porcentagem: float
    valor_diario: Union[float, int]


class DailyDonation(BaseModel):
    metodos_pagamento: Dict[str, PaymentMethod]
    total_arrecadado: Union[float, int]


class DailyDonationsResponse(BaseModel):
    daily_donations: Dict[str, DailyDonation] = Field(...)


class ErrorResponse(BaseModel):
    error: str


class DonationHour(BaseModel):
    doacoes: int
    porcentagem: float


class DonationsByHour(BaseModel):
    donations_by_hour: Dict[str, Union[DonationHour, ErrorResponse]]


class PaymentMethod(BaseModel):
    porcentagem: float
    quantidade_diaria: int


class DayDonation(BaseModel):
    metodos_pagamento: Dict[str, PaymentMethod]
    total_doacoes: int


class DailyDonationsByMethodResponse(BaseModel):
    donations_by_payment_method_per_day: Dict[str, DayDonation] = Field(...)


class PaymentMethod(BaseModel):
    porcentagem: Union[float, str]
    total_arrecadado: Union[float, int]


class MonthDonation(BaseModel):
    metodos_pagamento: Dict[str, PaymentMethod]
    total_arrecadado: Union[float, int]


class MonthlyDonationsResponse(BaseModel):
    donations_per_month: Dict[str, MonthDonation] = Field(...)


class AnonymousDonations(BaseModel):
    anonimo_percentage: str = Field(...)
    anonimo_total: str = Field(...)


class NonAnonymousDonations(BaseModel):
    nao_anonimo_percentage: str = Field(...)
    nao_anonimo_total: str = Field(...)


class DonationSummary(BaseModel):
    donations_anonymous: AnonymousDonations = Field(...)
    donations_non_anonymous: NonAnonymousDonations = Field(...)
    total_arrecadado: str = Field(...)


class CampaignData(BaseModel):
    meta_arrecadacao: Optional[float]
    percentual_meta_alcancada: Optional[float]
    titulo: str
    valor_arrecadado: str


class CampaignsResponse(BaseModel):
    campaigns_data: List[CampaignData]


class LatestDonation(BaseModel):
    cpf_usuario: str
    data_hora: str
    forma_pagamento: str
    id_pedido: int
    nome_campanha: str
    nome_usuario: str
    status_pedido: int
    valor_doado: str


class LatestDonationsResponse(BaseModel):
    latest_donations: List[LatestDonation]


class DailyDonations(BaseModel):
    daily_donations: Dict[str, str]


class TopDonor(BaseModel):
    cpf_usuario: str
    clifor_id: int
    usuario_id: Optional[int]
    nome_usuario: str
    quantidade_doacoes: int
    total_doado: str


class TopDonors(BaseModel):
    top_donors: List[TopDonor]


class NameUsersDonations(BaseModel):
    names_users_donations: List[str]


class TotalDonations(BaseModel):
    valor_total: str


class TotalDonationsDaily(BaseModel):
    total_do_dia: str


class MediaMensal(BaseModel):
    media_quant_mensal: int
    media_valor_mensal: str


class MediaDiaria(BaseModel):
    media_valores_diaria: str
    media_quantidade_diaria: int


class DonationItem(BaseModel):
    benfeitor: str
    quantidade_doacoes: int
    user_id: int
    valor: str


class DonationActualMonth(BaseModel):
    res: List[DonationItem]


class ResItem(BaseModel):
    nome: str
    user_id: int
    valor_doado: float


class Pagination(BaseModel):
    page: int
    per_page: int
    total: int


class UserTotalDonations(BaseModel):
    valor_doado: str
    quant_doacoes: int
