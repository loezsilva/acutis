import uuid
from datetime import datetime

from pydantic import BaseModel


class RegistrarDoacaoAnonimaSchema(BaseModel):
    benfeitor_id: uuid.UUID
    campanha_doacao_id: uuid.UUID | None
    valor_pagamento: float
    data_pagamento: datetime
    codigo_transacao: str
    codigo_comprovante: str


class BuscarDadosDoacaoSchema(BaseModel):
    nome: str
    email: str
    foto_campanha: str
    nome_campanha: str
