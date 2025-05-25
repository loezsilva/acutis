from typing import List
from pydantic import BaseModel


class SendReminderUnpaidDonationRequest(BaseModel):
    lista_processamento_pedido: List[int]
