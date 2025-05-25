from typing import Optional
from pydantic import BaseModel


class UserActiveAccountResponse(BaseModel):
    access_token: Optional[str]
    refresh_token: Optional[str]
    campanha_origem: Optional[int]
    usuario_id: Optional[int]
    email: Optional[str]
    telefone: Optional[str]
    nome: Optional[str]
