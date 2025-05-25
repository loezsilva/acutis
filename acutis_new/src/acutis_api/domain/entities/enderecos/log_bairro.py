from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from acutis_api.domain.database import table_registry


@table_registry.mapped_as_dataclass
class LogBairro:
    __bind_key__ = 'enderecos'
    __tablename__ = 'log_bairro'

    bai_nu: Mapped[int] = mapped_column(init=False, primary_key=True)
    ufe_sg: Mapped[str] = mapped_column(String(2))
    loc_nu: Mapped[int]
    bai_no: Mapped[str] = mapped_column(String(72))
    bai_no_abrev: Mapped[str] = mapped_column(String(36))
