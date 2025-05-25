from pydantic import BaseModel

class InfoCard(BaseModel):
    total_items: int
    valor_total: str
    
class Paginate(BaseModel):
    current_page: int
    per_page: int
    total_items: int

class ListDonationsRecurrences(BaseModel):
    campanha: str
    clifor_id: int
    pedido_id: int
    data_donation: str
    metodo_pagamento: str
    nome: str
    valor: str
    
class ResponseDonationsRecurrenceMade(BaseModel):
    lista: list[ListDonationsRecurrences]
    pagination: Paginate
    info_card: InfoCard