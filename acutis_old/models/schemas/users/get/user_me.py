from typing import Optional
from pydantic import BaseModel, EmailStr


class UserMeResponse(BaseModel):
    id: int
    nome: Optional[str]
    nome_social: Optional[str]
    email: Optional[EmailStr]
    numero_documento: Optional[str]
    data_nascimento: Optional[str]
    telefone: Optional[str]
    sexo: Optional[str]
    avatar: Optional[str]
    pais: Optional[str]
    fk_perfil_id: Optional[int]
    fk_clifor_id: Optional[int]
    obriga_atualizar_endereco: Optional[bool]
    obriga_atualizar_cadastro: Optional[bool]
    campanha_origem: Optional[int]
    super_perfil: Optional[bool]

    class Config:
        orm_mode = True
