from enum import Enum
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, SecretStr, validator


class TipoDocumentoEnum(str, Enum):
    cpf = "cpf"
    cnpj = "cnpj"
    identidade_estrangeira = "identidade_estrangeira"


class RegisterUserRequest(BaseModel):
    pais: str = Field(..., min_length=3, max_length=50, description="Nome do país")
    nome: str = Field(..., min_length=6, max_length=100, description="Nome completo")
    email: EmailStr = Field(..., description="Email do usuário")
    password: SecretStr = Field(
        ...,
        min_length=8,
        max_length=16,
        description="Senha do usuário",
    )
    numero_documento: str = Field(
        ..., min_length=6, max_length=20, description="Número do documento"
    )
    tipo_documento: TipoDocumentoEnum
    campanha_origem: Optional[int]

    @validator("password")
    def validar_password(cls, value: SecretStr):
        senha = value.get_secret_value()
        if not any(char.isdigit() for char in senha):
            raise ValueError("A senha deve conter pelo menos um número.")
        if not any(char.isupper() for char in senha):
            raise ValueError("A senha deve conter pelo menos uma letra maiúscula.")
        if not any(char.islower() for char in senha):
            raise ValueError("A senha deve conter pelo menos uma letra minúscula.")
        if not any(char in "@$!%*#?&" for char in senha):
            raise ValueError("A senha deve conter pelo menos um caractere especial.")
        return value
