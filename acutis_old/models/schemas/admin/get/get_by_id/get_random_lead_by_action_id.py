from typing import Optional
from pydantic import BaseModel


class GetRandomLeadByActionIdResponse(BaseModel):
    nome: Optional[str]
    telefone: Optional[str]
    email: Optional[str]
    cadastrado_em: Optional[str]

    class Config:
        orm_mode = True
