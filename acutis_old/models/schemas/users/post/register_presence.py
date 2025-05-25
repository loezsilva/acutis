from typing import Optional
from pydantic import BaseModel, Field


class RegisterPresenceRequest(BaseModel):
    fk_campanha_id: int = Field(..., description="ID da campanha")
    fk_landpage_id: Optional[int] = Field(None, description="ID da landpage")
