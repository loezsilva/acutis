from datetime import date
from typing import List, Optional
from pydantic import BaseModel, EmailStr, validator
from datetime import datetime

class GetAllUsersSchema(BaseModel):
    id: Optional[int]
    nome: Optional[str]
    email: Optional[EmailStr]
    status: Optional[bool]
    data_criacao: Optional[str]   

    @validator('data_criacao', pre=True)
    def parse_data_criacao(cls, value):
        if isinstance(value, datetime):
            return value.strftime("%d/%m/%Y %H:%M:%S")   
        return value

    class Config:
        orm_mode = True


class GetAllUsersResponse(BaseModel):
    page: int
    pages: int
    total: int
    usuarios: List[GetAllUsersSchema]


class GetAllUsersQuery(BaseModel):
    page: Optional[int] = 1
    per_page: Optional[int] = 10
    filtro_id_usuario: Optional[str]
    filtro_numero_documento: Optional[str]
    filtro_status: Optional[bool]
    filtro_email: Optional[str]
    filtro_nome: Optional[str]
    filtro_campanha_origem: Optional[str]
    filtro_telefone: Optional[str]
    filtro_data_cadastro_inicial: Optional[date]
    filtro_data_cadastro_final: Optional[date]
    filtro_data_ultimo_acesso_inicial: Optional[date]
    filtro_data_ultimo_acesso_final: Optional[date]
