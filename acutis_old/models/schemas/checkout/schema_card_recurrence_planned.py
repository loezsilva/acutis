from pydantic import BaseModel

class ReponseCardRecurrencePlanned(BaseModel):
    quantidade: int
    valor: str