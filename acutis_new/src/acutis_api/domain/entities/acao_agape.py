from enum import Enum

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from acutis_api.domain.database import table_registry
from acutis_api.domain.entities.modelo_base import ModeloBase


class PerfisAgape(str, Enum):
    voluntario = 'voluntario agape'
    administrador = 'administrador agape'


@table_registry.mapped_as_dataclass
class AcaoAgape(ModeloBase):
    __tablename__ = 'acoes_agape'

    nome: Mapped[str] = mapped_column(String, nullable=False)
