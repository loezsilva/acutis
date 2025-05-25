import uuid

from pydantic import BaseModel, ConfigDict


class RegistrarNovoMembroResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    nome: str


class RegistrarNovoLeadResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    nome: str
