from typing import Optional
from click import Option
from pydantic import BaseModel, Field


class ListarDoacoesQuery(BaseModel):
    cancelada_por: str = Field(None, description="Id do usuário que cancelou a recorrência caso tratar-se de uma doação recorrente")
    page: int = Field(None, description="Pagina atual")
    per_page: int = Field(None, description="Quantidade de items por página")
    filter_multiple: str = Field(None, description="Filtro para email, nome, cpf")
    tipo_pagamento: int = Field(None, description="Filtra por tipo de pagamento -> 1: Credito - 2: PIX - 3: Boleto")
    campanha_id: int = Field(None, description="ID de campanha")
    status: int = Field(None, description="Status do pagamento 1: pago - 0: em processamento -  2: não pago")
    data_inicial: str = Field(None, description="Data inicial")
    data_final: str = Field(None, description="Data final")
    nome_cliente: str = Field(None, description="Nome do cliente")
    recorrencia: str = Field(None, description="'recorrente' | 'nao_recorrente' ")
    doacao_anonima: str = Field(None, description="1: Anônima - 0: Idêntificada")
    transaction_id: str = Field(None, description="Id de transação")
    codigo_referencial: str = Field(None, description="Código de transferência")
    status_recorrencia: str = Field(None, description="'canceladas' - 'ativas' ")
    fk_gateway_pagamento_id: int = Field(None, description="1: itaú - 2: Mercado pago")
    email: str = Field(None, description="Email do usuário")
    cpf: str = Field(None, description="Cpf do usuário")
    pedido_id: str = Field(None, description="ID pedido")
    

class ListarDoacoesBenfeitorResponse(BaseModel):
    deleted_at: Optional[str]
    fk_clifor_id: int
    nome: str
    user_id: Optional[int]


class ListarDoacoesCampanhaResponse(BaseModel):
    descricao: Optional[str]
    fk_campanha_id: Optional[int]
    imagem: Optional[str]
    titulo: Optional[str]


class ListarDoacoesPedidoResponse(BaseModel):
    anonimo: bool
    contabilizar_doacao: bool
    cancelada_em: Optional[str]
    cancelada_por: Optional[str]
    data_doacao: Optional[str]
    fk_pedido_id: int
    forma_pagamento: str
    gateway_pagamento: dict
    order_id: Optional[str]
    recorrencia: bool
    recorrencia_ativa: bool
    status_pedido: int
    valor_doacao: str
    

class ListarDoacoesProcessamentoPedidoResponse(BaseModel):
    codigo_referencia: str
    fk_processamento_pedido_id: int
    id_pagamento: Optional[str]
    status: str
    transaction_id: Optional[str]
    
    
class DoacaoResponse(BaseModel):
    benfeitor: ListarDoacoesBenfeitorResponse
    campanha: ListarDoacoesCampanhaResponse
    pedido: ListarDoacoesPedidoResponse
    processamento: ListarDoacoesProcessamentoPedidoResponse
    
class ListarDoacoesResponse(BaseModel):
    data: list[DoacaoResponse]
    page: int
    pages: int
    total: int
    total_doado: str 
    
       