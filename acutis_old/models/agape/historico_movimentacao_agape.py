from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from builder import db
from utils.functions import get_current_time


class TipoMovimentacaoEnum(str, Enum):
    entrada = "entrada"
    saida = "saida"


class HistoricoOrigemEnum(str, Enum):
    acao = "acao"
    aquisicao = "aquisicao"
    estoque = "estoque"


class HistoricoDestinoEnum(str, Enum):
    acao = "acao"
    doacao = "doacao"
    estoque = "estoque"


@dataclass
class HistoricoMovimentacaoAgape(db.Model):
    __tablename__ = "historico_movimentacoes_agape"

    id: int = db.Column(db.Integer, primary_key=True)
    fk_estoque_agape_id: int = db.Column(
        db.Integer,
        db.ForeignKey("estoque_agape.id"),
        nullable=False,
        index=True,
    )
    quantidade: int = db.Column(db.Integer, nullable=False)
    tipo_movimentacao: TipoMovimentacaoEnum = db.Column(
        db.String(10), nullable=False, index=True
    )
    origem: HistoricoOrigemEnum = db.Column(db.String(50), index=True)
    destino: HistoricoDestinoEnum = db.Column(db.String(50), index=True)
    fk_instancia_acao_agape_id: int = db.Column(
        db.Integer, db.ForeignKey("instancia_acao_agape.id"), index=True
    )
    created_at: datetime = db.Column(
        db.DateTime, default=get_current_time, index=True
    )
    updated_at: datetime = db.Column(db.DateTime)
