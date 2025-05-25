from pydantic import BaseModel, Field
from datetime import date


class StatsByQuery(BaseModel):
    initial_date: date = Field(None, description="Data inicial no formato 'YYYY-MM-DD'")
    final_date: date = Field(None, description="Data final no formato 'YYYY-MM-DD'")
    aggregated_by: str = Field(..., description="day | month")