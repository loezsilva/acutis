from pydantic import BaseModel


class GetTotalLeadsByActionIdResponse(BaseModel):
    total_leads: int
