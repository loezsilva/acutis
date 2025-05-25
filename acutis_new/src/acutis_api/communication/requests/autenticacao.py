import re

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    SecretStr,
    field_validator,
)
from pydantic_core import PydanticCustomError


def validar_requisitos_senha(value: str) -> str:
    if len(value) < 8 or len(value) > 16:  # noqa
        raise PydanticCustomError(
            'value_error', 'A senha deve conter entre 8 a 16 caracteres.'
        )
    if re.search(r'\s', value):
        raise PydanticCustomError(
            'value_error', 'A senha não pode conter espaços em branco.'
        )
    if not any(char.isdigit() for char in value):
        raise PydanticCustomError(
            'value_error', 'A senha deve conter pelo menos um número.'
        )
    if not any(char.isupper() for char in value):
        raise PydanticCustomError(
            'value_error',
            'A senha deve conter pelo menos uma letra maiúscula.',
        )
    if not any(char.islower() for char in value):
        raise PydanticCustomError(
            'value_error',
            'A senha deve conter pelo menos uma letra minúscula.',
        )
    if not any(char in '@$!%*#?&' for char in value):
        raise PydanticCustomError(
            'value_error',
            'A senha deve conter pelo menos um caractere especial.',
        )
    return value


class LoginRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    email: EmailStr
    senha: SecretStr


class UsarHttpOnlyQuery(BaseModel):
    httponly: bool | None = True


class VerificarTokenRequest(BaseModel):
    token: str


class AtivarContaRequest(VerificarTokenRequest):
    senha: SecretStr

    @field_validator('senha', mode='before')
    @classmethod
    def validar_senha(cls, value: str):
        return validar_requisitos_senha(value)


class RecuperarSenhaRequest(BaseModel):
    email: EmailStr = Field(..., description='Email do usuário')
    url_redirecionamento: str = Field(
        default='/autenticacao/trocar-senha',
        description='Url de redirecionamento',
    )


class AlterarSenhaRequest(BaseModel):
    senha_atual: SecretStr = Field(
        ...,
        min_length=8,
        max_length=16,
        description='Senha atual do usuário',
    )
    nova_senha: SecretStr = Field(
        ...,
        min_length=8,
        max_length=16,
        description='Nova senha do usuário',
    )

    @field_validator('nova_senha', mode='before')
    def validar_senha(cls, value: str):
        return validar_requisitos_senha(value)


class NovaSenhaQuery(BaseModel):
    token: str = Field(
        ..., description=('Token para validar o reset da senha')
    )


class NovaSenhaRequest(BaseModel):
    nova_senha: SecretStr = Field(
        ...,
        min_length=8,
        max_length=16,
        description='Nova senha do usuário',
    )

    @field_validator('nova_senha', mode='before')
    def validar_senha(cls, value: str):
        return validar_requisitos_senha(value)
