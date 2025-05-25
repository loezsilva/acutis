from typing import Optional, List
from pydantic import BaseModel

class RecorrenciaCancelada(BaseModel):
    benfeitor: str
    campanha: str
    cancelada_em: Optional[str]
    cancelada_por: Optional[str]
    data_pedido: str
    id: int
    metodo: str
    valor: str

class ListarRecorrenciasCanceladasResponse(BaseModel):
    card_qtd_doacoes: int
    card_soma_valor_doacoes: str
    doacoes_recorrentes_canceladas: List[RecorrenciaCancelada]
    page: int
    pages: int
    total: int