from typing import List
from pydantic import BaseModel


class DonationReceiptSchema(BaseModel):
    nome_acao: str
    fk_doacao_agape_id: int
    fk_instancia_acao_agape_id: int
    dia_horario: str
    recibos: List[str] | str

    class Config:
        orm_mode = True


class GetAllDonationsReceiptsResponse(BaseModel):
    total: int
    page: int
    doacoes_recebidas: List[DonationReceiptSchema]
