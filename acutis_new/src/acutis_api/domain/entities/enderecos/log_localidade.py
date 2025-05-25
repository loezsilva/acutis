from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from acutis_api.domain.database import table_registry


@table_registry.mapped_as_dataclass
class LogLocalidade:
    __bind_key__ = 'enderecos'
    __tablename__ = 'log_localidade'

    loc_nu: Mapped[int] = mapped_column(init=False, primary_key=True)
    ufe_sg: Mapped[str] = mapped_column(String(2))
    loc_no: Mapped[str] = mapped_column(String(72))
    cep: Mapped[str] = mapped_column(String(8))
    loc_in_sit: Mapped[str] = mapped_column(String(1))
    loc_in_tipo_loc: Mapped[str] = mapped_column(String(1))
    loc_nu_sub: Mapped[int]
    loc_no_abrev: Mapped[str] = mapped_column(String(36))
    mun_nu: Mapped[int]
