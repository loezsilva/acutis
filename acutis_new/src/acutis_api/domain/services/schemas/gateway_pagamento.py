from enum import Enum

from pydantic import BaseModel, field_validator


class TipoDocumentoEnum(str, Enum):
    CPF = 'cpf'
    CNPJ = 'cnpj'


class CriarPagamentoPixRequest(BaseModel):
    data_vencimento: str
    tipo_documento: TipoDocumentoEnum
    numero_documento: str
    nome: str
    valor_doacao: float
    chave_pix: str


class BuscarPagamentoPixResponse(BaseModel):
    pix_copia_cola: str
    qrcode: str
    transacao_id: str


class CriarPagamentoBolecodeRequest(BaseModel):
    valor_doacao: float | str
    nome: str
    numero_documento: str
    rua: str
    bairro: str
    cidade: str
    estado: str
    cep: str
    data_vencimento: str
    chave_pix: str

    @field_validator('valor_doacao')
    @classmethod
    def formatar_valor_doacao(cls, value: float) -> str:
        value = str(int(value * 100)).zfill(17)
        return value
