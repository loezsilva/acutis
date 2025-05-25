from typing import List
from pydantic import BaseModel, Field
from spectree import BaseFile


class RegisterAgapeDonationReceiptsFormData(BaseModel):
    recibos: List[BaseFile] | BaseFile = Field(..., min_items=1, max_items=2)
