from typing import Optional
from pydantic import BaseModel


class GetAgapeMemberResponse(BaseModel):
    id: int
    nome: str
    email: Optional[str] = None
    telefone: Optional[str] = None
    cpf: Optional[str] = None
    data_nascimento: str
    responsavel: bool
    funcao_familiar: str
    escolaridade: str
    ocupacao: str
    renda: float | None
    foto_documento: str | None
    beneficiario_assistencial: bool | None

    class Config:
        orm_mode = True