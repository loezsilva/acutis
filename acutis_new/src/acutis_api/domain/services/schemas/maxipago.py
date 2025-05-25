from pydantic import BaseModel, ConfigDict


class DadosPagamento(BaseModel):
    codigo_referencia: str
    numero_documento: str
    nome: str
    rua: str
    bairro: str
    cidade: str
    estado: str
    cep: str
    telefone: str
    email: str
    numero_cartao: str
    vencimento_mes: str
    vencimento_ano: str
    codigo_seguranca: str
    valor_doacao: float


class PagamentoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra='ignore')

    orderID: str
    referenceNum: str
    transactionID: str
