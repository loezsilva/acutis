from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Item(BaseModel):
    cpf_cnpj: str
    data_inclusao: datetime   
    fk_clifor_id: int
    fk_usuario_id: Optional[int]   
    incluido_por: int
    nome: str

class Pagination(BaseModel):
    page: int
    per_page: int
    total_items: int

class ResponseDonationsExceptions(BaseModel):
    pagination: Pagination
    res: List[Item]
