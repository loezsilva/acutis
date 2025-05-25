from typing import Optional
from pydantic import BaseModel


class GetCardTotalDonationsReceiptsResponse(BaseModel):
    total_itens_recebidos: Optional[str]
