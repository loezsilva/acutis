from enum import Enum
from pydantic import BaseModel, Field


class TipoDocumentoEnum(str, Enum):
    cpf = "cpf"
    cnpj = "cnpj"
    identidade_estrangeira = "identidade_estrangeira"


class GetCpfRegistrationStatusQuery(BaseModel):
    tipo_documento: TipoDocumentoEnum = Field(
        ..., description="Tipo de documento utilizado pelo usuário"
    )
    numero_documento: str = Field(
        ..., description="Número do documento utilizado pelo usuário"
    )


class GetCpfRegistrationStatusResponse(BaseModel):
    possui_conta: bool = Field(
        description="Retorna se o usuário possui uma conta no CPF informado"
    )
    atualizar_conta: bool = Field(
        description="Retorna se o usuário deve atualizar sua conta"
    )
