import uuid

from pydantic import BaseModel


class RegistrarNovoMembroOficialResponse(BaseModel):
    uuid: uuid.UUID
    criado_em: str
