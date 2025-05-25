from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime


class Endereco(BaseModel):
    rua: Optional[str]
    cep: Optional[str]
    estado: Optional[str]
    complemento: Optional[str]
    bairro: Optional[str]
    numero: Optional[str]
    cidade: Optional[str]


class GeneralResponse(BaseModel):
    id: int
    nome: str
    telefone: Optional[str]
    email: Optional[str]
    created_at: str
    rua: Optional[str]
    cep: Optional[str]
    estado: Optional[str]
    complemento: Optional[str]
    bairro: Optional[str]
    numero: Optional[str]
    cidade: Optional[str]
    quant_membros_grupo: Optional[int]
    updated_at: Optional[datetime]   
    tempo_de_administrador: Optional[int]
    link_grupo: Optional[str]
    nome_grupo: Optional[str]
    usuario_superior: Optional[str]
    cargo: Optional[str]
    status: Optional[str]


class Paginate(BaseModel):
    page: int
    per_page: int
    total: int


class ResponseGetAllGenerais(BaseModel):
    list: List[GeneralResponse]
    paginate: Paginate
    count_generais: int
    count_marechais: int


class QuerysGetAllGenerais(BaseModel):
    page: int = 1   
    per_page: int = 10   

    general_id: Optional[str] = Field(None, description="Id do general")
    nome: Optional[str] = Field(None, description="Nome do general") 
    email: Optional[str] = Field(None, description="Email do general")
    telefone: Optional[str] = Field(None, description="Telefone do general")
    cargo: Optional[str] = Field(None, description="``` 1: Marechal - 2: General```")
    fk_superior_id: Optional[int] = Field(None, description="Id do marechal")
    data_inicio: Optional[str] = Field(None, description="Data de cadastro inicial")
    data_fim: Optional[str] = Field(None, description="Data de cadastro final")
    status: Optional[str] = Field(None, description="True: aprovado - False: recusado")