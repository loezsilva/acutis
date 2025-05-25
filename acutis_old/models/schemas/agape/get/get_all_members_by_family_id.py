from typing import List, Optional
from pydantic import BaseModel


class FamilyMemberSchema(BaseModel):
    id: int
    nome: str
    telefone: Optional[str]
    email: Optional[str]
    cpf: Optional[str]
    idade: int
    ocupacao: Optional[str]
    renda: Optional[float]
    responsavel: bool

    class Config:
        orm_mode = True


class GetAllMembersByFamilyIdResponse(BaseModel):
    page: int
    total: int
    membros: List[FamilyMemberSchema]
