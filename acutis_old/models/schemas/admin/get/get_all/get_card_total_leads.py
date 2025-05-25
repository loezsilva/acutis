from pydantic import BaseModel


class GetCardTotalLeadsResponse(BaseModel):
    total_leads: int
    leads_cadastrados: int
    leads_unicos: int
