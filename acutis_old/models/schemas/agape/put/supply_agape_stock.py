from pydantic import BaseModel, Field


class SupplyAgapeStockRequest(BaseModel):
    quantidade: int = Field(..., gt=0, description="Quantidade do item")
