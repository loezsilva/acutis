import uuid
from typing import Optional

from pydantic import BaseModel


class SuperioresSchema(BaseModel):
    nome_superior: str


class BuscaCargoSuperiorResponse(BaseModel):
    superiores: Optional[list[SuperioresSchema]] = None
    cargo_superior: str
    fk_cargo_superior_id: uuid.UUID
