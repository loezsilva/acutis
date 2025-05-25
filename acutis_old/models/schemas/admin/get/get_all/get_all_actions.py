from datetime import date
from typing import Optional
from pydantic import BaseModel, Field

from utils.functions import get_current_time


class GetAllActionsFilters(BaseModel):
    page: Optional[int] = Field(
        1, description="Declara a página em que deseja buscar as informações"
    )
    per_page: Optional[int] = Field(
        10, description="Declara a quantidade de itens por página"
    )
    filtro_acao_id: Optional[int] = Field(None, description="Filtra pelo ID da ação")
    filtro_nome: Optional[str] = Field(None, description="Filtra pelo nome da ação")
    filtro_data_inicial: Optional[date] = Field(
        None, description="Filtra pelo intervalo inicial da data de criação da ação"
    )
    filtro_data_final: Optional[date] = Field(
        get_current_time().date(),
        description="Filtra pelo intervalo final da data de criação da ação",
    )


class GetAllActionsSchema(BaseModel):
    id: int
    nome: Optional[str]
    quantidade_leads: Optional[int]
    criada_em: Optional[str]
    status: bool
    sorteio: Optional[bool]

    class Config:
        orm_mode = True


class GetAllActionsResponse(BaseModel):
    page: int
    total: int
    acoes: list[GetAllActionsSchema]
