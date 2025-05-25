import uuid
from enum import Enum

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from acutis_api.domain.database import table_registry
from acutis_api.domain.entities.modelo_base import ModeloBase


class TipoMovimentacaoEnum(str, Enum):
    entrada = 'entrada'
    saida = 'saida'


class HistoricoOrigemEnum(str, Enum):
    acao = 'acao'
    aquisicao = 'aquisicao'
    estoque = 'estoque'


class HistoricoDestinoEnum(str, Enum):
    acao = 'acao'
    doacao = 'doacao'
    estoque = 'estoque'


@table_registry.mapped_as_dataclass
class HistoricoMovimentacaoAgape(ModeloBase):
    __tablename__ = 'historicos_movimentacoes_agape'

    fk_estoque_agape_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('estoques_agape.id'), index=True
    )
    quantidade: Mapped[int]
    tipo_movimentacoes: Mapped[TipoMovimentacaoEnum] = mapped_column(
        index=True
    )
    origem: Mapped[HistoricoOrigemEnum | None] = mapped_column(index=True)
    destino: Mapped[HistoricoDestinoEnum | None] = mapped_column(index=True)
    fk_instancia_acao_agape_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey('instancias_acoes_agape.id'), index=True
    )
