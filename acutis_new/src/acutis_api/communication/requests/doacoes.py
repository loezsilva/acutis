import re
import uuid

from pydantic import BaseModel, ConfigDict, Field, field_validator
from pydantic_core import PydanticCustomError

REGEX_NOME = r'^[a-zA-ZáÁâÂãÃàÀéÉêÊèÈíÍóÓôÔõÕúÚùÙçÇ\s]+$'


class DadosDoacaoBase(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    valor_doacao: float = Field(..., ge=10)
    campanha_id: uuid.UUID

    @field_validator('valor_doacao', mode='before')
    @classmethod
    def validar_valor_doacao(cls, value: float):
        if value < 10.0:  # noqa
            raise PydanticCustomError(
                'value_error', 'O valor deve ser maior ou igual a R$ 10,00.'
            )
        return value


class RegistrarDoacaoCartaoCreditoRequest(DadosDoacaoBase):
    numero_cartao: str
    vencimento_mes: str = Field(..., min_length=2, max_length=2)
    vencimento_ano: str = Field(..., min_length=4, max_length=4)
    codigo_seguranca: str = Field(..., min_length=3, max_length=4)
    nome_titular: str
    numero_documento: str
    recorrente: bool

    @field_validator('numero_cartao', 'numero_documento', mode='after')
    @classmethod
    def formatar_numero(cls, value: str):
        value = ''.join(filter(str.isdigit, value))
        return value

    @field_validator('nome_titular', mode='after')
    @classmethod
    def validar_nome(cls, value: str):
        if not bool(re.match(REGEX_NOME, value)):
            raise PydanticCustomError(
                'value_error', f'O nome {value} possui caracteres inválidos.'
            )
        return value.title()


class RegistrarDoacaoPixRequest(DadosDoacaoBase):
    recorrente: bool


class RegistrarDoacaoBoletoRequest(DadosDoacaoBase): ...


class PagamentoPixRecorrenteTokenQuery(BaseModel):
    token: str
