from datetime import date
from typing import List, Optional
from pydantic import BaseModel, Field


class GetAllLeadsQuery(BaseModel):
    page: Optional[int] = Field(
        gt=0, description="Declara a página em que deseja buscar as informações"
    )
    per_page: Optional[int] = Field(
        default=10, gt=0, description="Declara a quantidade de itens por página"
    )
    filtro_nome: Optional[str]
    filtro_email: Optional[str]
    filtro_origem: Optional[str]
    filtro_data_inicial: Optional[date]
    filtro_data_final: Optional[date]
    filtro_nao_baixadas: Optional[bool] = False


class GetAllLeadsSchema(BaseModel):
    id: int
    nome: Optional[str]
    email: Optional[str]
    telefone: Optional[str]
    origem: Optional[str]
    criacao: Optional[str]
    download: Optional[str]
    sorteado: Optional[bool]
    download_usuario_id: Optional[int]
    foto: Optional[str]
    intencao: Optional[str]

    class Config:
        orm_mode = True


class GetAllLeadsResponse(BaseModel):
    page: int
    total: int
    leads: List[GetAllLeadsSchema]
