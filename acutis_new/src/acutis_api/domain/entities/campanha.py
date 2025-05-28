import uuid
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from acutis_api.domain.database import table_registry

if TYPE_CHECKING:
    from acutis_api.domain.entities import (  # pragma: no cover
        CampanhaDoacao,
        CampoAdicional,
        LandingPage,
        Membro,
    )


class ObjetivosCampanhaEnum(str, Enum):
    pre_cadastro = 'pre_cadastro'
    cadastro = 'cadastro'
    doacao = 'doacao'
    oficiais = 'oficiais'


@table_registry.mapped_as_dataclass
class Campanha:
    __tablename__ = 'campanhas'

    id: Mapped[uuid.UUID] = mapped_column(
        init=False, primary_key=True, default_factory=uuid.uuid4
    )
    fk_cargo_oficial_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey('cargos_oficiais.id'), index=True
    )
    objetivo: Mapped[ObjetivosCampanhaEnum] = mapped_column(index=True)
    nome: Mapped[str]
    publica: Mapped[bool] = mapped_column(index=True)
    ativa: Mapped[bool] = mapped_column(index=True)
    meta: Mapped[float | None]
    capa: Mapped[str | None]
    chave_pix: Mapped[str | None]
    criado_em: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    criado_por: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey('membros.id'),
        nullable=True,
    )
    atualizado_em: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )
    superior_obrigatorio: Mapped[bool] = mapped_column(
        index=True, default=False
    )

    membro: Mapped['Membro'] = relationship(init=False, backref='campanha')
    landing_page: Mapped['LandingPage'] = relationship(
        init=False, backref='campanha'
    )
    campos_adicionais: Mapped[list['CampoAdicional']] = relationship(
        init=False, back_populates='campanha'
    )
    campanha_doacao: Mapped['CampanhaDoacao'] = relationship(
        init=False, backref='campanha'
    )
