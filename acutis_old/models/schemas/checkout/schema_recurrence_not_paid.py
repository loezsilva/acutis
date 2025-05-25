from typing import Optional
from pydantic import BaseModel, Field


class Donations(BaseModel):
    campanha: str
    clifor_id: int
    data_lembrete_doacao: Optional[str]
    data_prevista: str
    lembrete_enviado_por: Optional[str]
    metodo_pagamento: str
    nome: str
    pedido_criado_em: str
    pedido_id: int
    processada_em: str
    valor: str
    
class Pagination(BaseModel):
    current_page: int
    per_page: int
    total_items: int
    total_pages: int

class DonaitonsNotPaid(BaseModel):
    lista: list[Donations]
    pagination: Pagination    
    
class ListagemDeRecorreciaEmLapsosRequest(BaseModel):
    per_page: int = Field(default=10, description="Quantidade por página")
    page: int = Field(default=1, description="Página")
    nome: str = Field(None, description="Nome do befeitor")
    data_inicial: str = Field(None, description="Data inicial")
    data_final: str = Field(None, description="Data final")
    campanha_id: str = Field(None, description="Filtrar por campanha")

