from typing import Optional

from pydantic import BaseModel


class GetUserByIdResponse(BaseModel):
    id: int
    nome: Optional[str]
    nome_social: Optional[str]
    email: Optional[str]
    pais: Optional[str]
    origem_cadastro: Optional[str]
    status: Optional[bool]
    data_cadastro: Optional[str]
    ultimo_acesso: Optional[str]
    avatar: Optional[str]
    numero_documento: Optional[str]
    telefone: Optional[str]
    perfil: Optional[str]

    class Config:
        orm_mode = True
