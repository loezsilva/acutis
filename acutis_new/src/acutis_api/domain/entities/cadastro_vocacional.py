import uuid
from datetime import date, datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from acutis_api.domain.database import table_registry


@table_registry.mapped_as_dataclass
class CadastroVocacional:
    __tablename__ = 'cadastros_vocacional'

    id: Mapped[uuid.UUID] = mapped_column(
        init=False, primary_key=True, default_factory=uuid.uuid4, index=True
    )
    fk_usuario_vocacional_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('usuarios_vocacional.id'), index=True, unique=True
    )
    fk_endereco_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('enderecos.id'), nullable=False, index=True
    )
    data_nascimento: Mapped[date] = mapped_column(nullable=False)
    documento_identidade: Mapped[str] = mapped_column(nullable=False)
    criado_em: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    atualizado_em: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )
