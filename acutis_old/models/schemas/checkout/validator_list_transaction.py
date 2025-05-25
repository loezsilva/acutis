from typing import Optional
from pydantic import BaseModel


class TransactionsSchema(BaseModel):
    data: Optional[str]
    id: int
    metodo: Optional[str]
    status: Optional[int]
    transaction_id: Optional[str]
    valor: Optional[str]


class ResponseListTransaction(BaseModel):
    page: int
    pages: int
    total: int
    transacoes: list[TransactionsSchema]
