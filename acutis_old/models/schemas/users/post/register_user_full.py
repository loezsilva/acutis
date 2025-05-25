from datetime import date
from enum import Enum
import json
from typing import Optional
from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    SecretStr,
    root_validator,
    validator,
)
from spectree import BaseFile


class GendersEnum(str, Enum):
    masculino = "masculino"
    feminino = "feminino"


class DocumentTypesEnum(str, Enum):
    CPF = "cpf"
    CNPJ = "cnpj"
    IDENTIDADE_ESTRANGEIRA = "identidade_estrangeira"


class RedirectPagesEnum(str, Enum):
    MEMBRO_EXERCITO = "membro-exercito"
    PRINCIPAL = "principal"


class RegisterUserFullDataSchema(BaseModel):
    nome: str = Field(
        ..., min_length=6, max_length=100, description="Nome completo"
    )
    nome_social: Optional[str] = Field(
        None,
        max_length=45,
        description="Nome que o usuário deseja ser chamado",
        error_messages={
            "value_error.any_str.max_length": "O nome social deve ter no máximo 45 caracteres"
        },
    )
    email: EmailStr = Field(..., description="Email do usuário")
    numero_documento: str = Field(
        ..., min_length=6, max_length=20, description="Número do documento"
    )
    tipo_documento: DocumentTypesEnum
    data_nascimento: Optional[date] = Field(
        None, description="Data de nascimento do usuário"
    )
    telefone: Optional[str] = Field(
        None,
        min_length=6,
        max_length=30,
        description="Celular ou telefone do benfeitor",
    )
    sexo: Optional[GendersEnum] = Field(None, description="Sexo do benfeitor")
    password: SecretStr = Field(
        ...,
        min_length=8,
        max_length=16,
        description="Senha do usuário",
    )
    campanha_origem: Optional[int] = None

    @validator("password")
    def validar_password(cls, value: SecretStr):
        senha = value.get_secret_value()
        if not any(char.isdigit() for char in senha):
            raise ValueError("A senha deve conter pelo menos um número.")
        if not any(char.isupper() for char in senha):
            raise ValueError(
                "A senha deve conter pelo menos uma letra maiúscula."
            )
        if not any(char.islower() for char in senha):
            raise ValueError(
                "A senha deve conter pelo menos uma letra minúscula."
            )
        if not any(char in "@$!%*#?&" for char in senha):
            raise ValueError(
                "A senha deve conter pelo menos um caractere especial."
            )
        return value


class RegisterUserAddressSchema(BaseModel):
    cep: Optional[str] = Field(None, min_length=8, max_length=9)
    rua: Optional[str] = Field(None, max_length=100)
    numero: Optional[str] = Field(None, max_length=8)
    complemento: Optional[str] = Field(None, max_length=60)
    ponto_referencia: Optional[str] = Field(None, max_length=100)
    bairro: Optional[str] = Field(None, max_length=80)
    estado: Optional[str] = Field(None, min_length=2, max_length=2)
    cidade: Optional[str] = Field(None, min_length=3, max_length=32)
    detalhe_estrangeiro: Optional[str] = Field(
        None,
        max_length=100,
        description="Campo preenchido caso o benfeitor não resida no Brasil.",
    )


class RegisterUserFullFormData(BaseModel):
    image: Optional[BaseFile] = Field(None, description="Imagem do usuário")
    pais: Optional[str] = Field(
        None, min_length=3, max_length=50, description="Nome do país"
    )
    pagina_redirecionamento: Optional[RedirectPagesEnum] = Field(
        RedirectPagesEnum.PRINCIPAL,
        description="Pagina onde o usuário será redirecionado após ativar a conta pelo link recebido por email.",
    )
    usuario: RegisterUserFullDataSchema
    endereco: RegisterUserAddressSchema

    @root_validator(pre=True)
    def validate_data(cls, values):
        if "usuario" in values and isinstance(values["usuario"], str):
            try:
                values["usuario"] = json.loads(values["usuario"])
            except json.JSONDecodeError:
                raise ValueError("O campo 'usuario' deve ser um JSON válido.")

        if "endereco" in values and isinstance(values["endereco"], str):
            try:
                values["endereco"] = json.loads(values["endereco"])
            except json.JSONDecodeError:
                raise ValueError("O campo 'endereco' deve ser um JSON valido.")
        return values
