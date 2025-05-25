from typing import Optional
from pydantic import BaseModel


class GetCardAgapeFamilyIncomeResponse(BaseModel):
    renda_familiar: Optional[str]
    renda_per_capta: Optional[str]
