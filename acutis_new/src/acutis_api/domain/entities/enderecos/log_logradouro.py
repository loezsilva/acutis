from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from acutis_api.domain.database import table_registry


@table_registry.mapped_as_dataclass
class LogLogradouro:
    __bind_key__ = 'enderecos'
    __tablename__ = 'log_logradouro'

    log_nu: Mapped[int] = mapped_column(init=False, primary_key=True)
    ufe_sg: Mapped[str] = mapped_column(String(2))
    loc_nu: Mapped[int]
    bai_nu_ini: Mapped[int]
    bai_nu_fim: Mapped[int]
    log_no: Mapped[str] = mapped_column(String(100))
    log_complemento: Mapped[str] = mapped_column(String(100))
    cep: Mapped[str] = mapped_column(String(8))
    tlo_tx: Mapped[str] = mapped_column(String(36))
    log_sta_tlo: Mapped[str] = mapped_column(String(1))
    log_no_abrev: Mapped[str] = mapped_column(String(36))
