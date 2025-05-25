from typing import List, Optional
from pydantic import BaseModel


class GetAllBirthdaysSchema(BaseModel):
    id: Optional[int]
    foto: Optional[str]
    nome: Optional[str]
    email: Optional[str]
    data_nascimento: Optional[str]
    telefone: Optional[str]
    idade: Optional[int]


class GetAllBirthdaysResponse(BaseModel):
    page: int
    total: int
    aniversariantes: List[GetAllBirthdaysSchema]
