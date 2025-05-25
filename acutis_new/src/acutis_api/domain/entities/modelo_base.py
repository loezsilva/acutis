import uuid
from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

# Importa seu registry principal
from acutis_api.domain.database import table_registry


@table_registry.mapped_as_dataclass
class ModeloBase:
    __abstract__ = True

    id: Mapped[uuid.UUID] = mapped_column(
        init=False, primary_key=True, default_factory=uuid.uuid4
    )

    criado_em: Mapped[datetime] = mapped_column(
        init=False,
        server_default=func.now(),
    )

    atualizado_em: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )
