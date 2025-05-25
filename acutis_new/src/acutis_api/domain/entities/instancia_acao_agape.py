import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from acutis_api.domain.database import table_registry


class StatusAcaoAgapeEnum(str, Enum):
    nao_iniciado = 'nao_iniciado'
    em_andamento = 'em_andamento'
    finalizado = 'finalizado'


class AbrangenciaInstanciaAcaoAgapeEnum(str, Enum):
    cep = 'cep'
    rua = 'rua'
    bairro = 'bairro'
    cidade = 'cidade'
    estado = 'estado'
    sem_restricao = 'sem_restricao'


@table_registry.mapped_as_dataclass
class InstanciaAcaoAgape:
    __tablename__ = 'instancias_acoes_agape'

    id: Mapped[uuid.UUID] = mapped_column(
        init=False, primary_key=True, default_factory=uuid.uuid4
    )
    fk_endereco_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('enderecos.id'), index=True
    )
    fk_acao_agape_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('acoes_agape.id'), index=True
    )
    data_inicio: Mapped[datetime | None]
    data_termino: Mapped[datetime | None]
    status: Mapped[StatusAcaoAgapeEnum] = mapped_column(
        default=StatusAcaoAgapeEnum.nao_iniciado, index=True
    )
    abrangencia: Mapped[AbrangenciaInstanciaAcaoAgapeEnum] = mapped_column(
        default=AbrangenciaInstanciaAcaoAgapeEnum.sem_restricao, index=True
    )
    criado_em: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    atualizado_em: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )
    itens = relationship(
        'ItemInstanciaAgape',
        backref='instancia_acao_agape',
        lazy='dynamic',
        cascade='all, delete',
    )
