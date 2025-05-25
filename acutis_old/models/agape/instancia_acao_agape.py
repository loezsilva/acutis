from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from builder import db
from utils.functions import get_current_time


class StatusAcaoAgapeEnum(str, Enum):
    nao_iniciado = "nao_iniciado"
    em_andamento = "em_andamento"
    finalizado = "finalizado"


class AbrangenciaInstanciaAcaoAgapeEnum(str, Enum):
    cep = "cep"
    rua = "rua"
    bairro = "bairro"
    cidade = "cidade"
    estado = "estado"
    sem_restricao = "sem_restricao"


@dataclass
class InstanciaAcaoAgape(db.Model):
    __tablename__ = "instancia_acao_agape"

    id: int = db.Column(db.Integer, primary_key=True)
    fk_endereco_id: int = db.Column(
        db.Integer, db.ForeignKey("endereco.id"), nullable=False, index=True
    )
    fk_acao_agape_id: int = db.Column(
        db.Integer, db.ForeignKey("acao_agape.id"), nullable=False, index=True
    )
    status: StatusAcaoAgapeEnum = db.Column(
        db.String(20), default=StatusAcaoAgapeEnum.nao_iniciado, index=True
    )
    data_inicio: datetime = db.Column(db.DateTime)
    data_termino: datetime = db.Column(db.DateTime)
    abrangencia: AbrangenciaInstanciaAcaoAgapeEnum = db.Column(
        db.String(20),
        default=AbrangenciaInstanciaAcaoAgapeEnum.sem_restricao,
        index=True,
    )
    created_at: datetime = db.Column(db.DateTime, default=get_current_time)
    updated_at: datetime = db.Column(db.DateTime)

    itens = db.relationship(
        "ItemInstanciaAgape",
        backref="instancia_acao_agape",
        lazy="dynamic",
        cascade="all, delete",
    )
