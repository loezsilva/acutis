from pydantic import BaseModel
from typing import List

class Donation(BaseModel):
    campanha: str
    clifor_id: int
    data_donation: str   
    metodo_pagamento: str
    nome: str
    pedido_id: int
    valor: str   

class Pagination(BaseModel):
    current_page: int
    pages: int
    per_page: int
    total_items: int

class ResponsePlanned(BaseModel):
    lista: List[Donation]
    pagination: Pagination
