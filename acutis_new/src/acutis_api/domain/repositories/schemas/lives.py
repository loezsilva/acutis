import uuid
from datetime import date
from typing import Optional

from pydantic import BaseModel


class ObterAudienciaLivesSchema(BaseModel):
    live_id: uuid.UUID
    data_inicial: Optional[date]
    data_final: Optional[date]
