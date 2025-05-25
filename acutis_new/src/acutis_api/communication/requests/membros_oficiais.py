import uuid
from typing import Optional

from pydantic import BaseModel, Field


class RegistrarMembroOficialRequest(BaseModel):
    fk_membro_id: uuid.UUID = Field(..., description='ID de membro')
    fk_superior_id: Optional[uuid.UUID] = Field(
        None, description='ID de membro superior'
    )
    fk_cargo_oficial_id: uuid.UUID = Field(
        ..., description='ID do cargo oficial'
    )
