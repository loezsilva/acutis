from pydantic import BaseModel, ConfigDict
from typing import List, Optional, Union

class GatewayPagamento(BaseModel):
    id: int
    nome: str

class Benfeitor(BaseModel):
    deleted_at: Optional[str]  
    fk_clifor_id: int
    nome: str
    user_id: Optional[int] 

class Campanha(BaseModel):
    descricao: Optional[str]  
    fk_campanha_id: Optional[int]  
    imagem: Optional[str]  
    titulo: Optional[str]  

class Pedido(BaseModel):
    anonimo: bool
    cancelada_em: Optional[str]  
    contabilizar_doacao: bool
    data_doacao: str
    fk_pedido_id: int
    forma_pagamento: str
    gateway_pagamento: GatewayPagamento
    order_id: Optional[str]  
    recorrencia: bool
    recorrencia_ativa: bool
    status_pedido: int
    valor_doacao: Union[str, float]

class Processamento(BaseModel):
    codigo_referencia: str
    fk_processamento_pedido_id: int
    id_pagamento: Optional[str]  
    status: str
    transaction_id: str

class DonationEntry(BaseModel):
    benfeitor: Benfeitor
    campanha: Campanha
    pedido: Pedido
    processamento: Processamento

class DonationResponse(BaseModel):
    data: List[DonationEntry]
    page: int
    pages: int
    total: int
    total_doado: str