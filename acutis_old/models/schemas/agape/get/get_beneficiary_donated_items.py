from pydantic import BaseModel


class DonatedItemSchema(BaseModel):
    item: str
    quantidade: int

    class Config:
        orm_mode = True


class GetBeneficiaryDonatedItemsResponse(BaseModel):
    itens_doados: list[DonatedItemSchema]
