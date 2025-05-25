from typing import List
from pydantic import BaseModel, Field


class DownloadLeadsPhotosRequest(BaseModel):
    ids_leads: List[int] = Field(
        ..., description="Lista com os IDs de leads que tiveram suas fotos baixadas"
    )
