from pydantic import BaseModel


class ItemReceiptSchema(BaseModel):
    item: str
    quantidade: int

    class Config:
        orm_mode = True


class GetAllItemsReceiptsResponse(BaseModel):
    itens_recebidos: list[ItemReceiptSchema]
