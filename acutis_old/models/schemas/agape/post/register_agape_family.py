from datetime import date
import json
from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    constr,
    root_validator,
    validator,
)
from spectree import BaseFile


class FamilyAddressSchema(BaseModel):
    cep: constr(min_length=8, max_length=9, strip_whitespace=True)  # type: ignore
    rua: constr(
        min_length=3, max_length=100, strip_whitespace=True
    )  # type: ignore
    numero: str | None = Field(None, max_length=8)
    complemento: str | None = Field(None, max_length=60)
    ponto_referencia: str | None = Field(None, max_length=100)
    bairro: constr(min_length=3, max_length=80, strip_whitespace=True)  # type: ignore
    cidade: constr(min_length=3, max_length=32, strip_whitespace=True)  # type: ignore
    estado: constr(min_length=2, max_length=2, strip_whitespace=True)  # type: ignore


class FamilyMemberSchema(BaseModel):
    responsavel: bool | None = False
    nome: constr(min_length=3, max_length=100, strip_whitespace=True)  # type: ignore
    email: EmailStr | None = None
    telefone: str | None = Field(None, max_length=20)
    cpf: str | None = Field(None, max_length=14)
    data_nascimento: date
    funcao_familiar: constr(min_length=3, max_length=50, strip_whitespace=True)  # type: ignore
    escolaridade: constr(min_length=5, max_length=50, strip_whitespace=True)  # type: ignore
    ocupacao: constr(min_length=3, max_length=100, strip_whitespace=True)  # type: ignore
    renda: float | None = None
    beneficiario_assistencial: bool
    foto_documento: str | None = None

    @validator("email")
    def check_email_length(cls, value):
        if value and len(value) > 100:
            raise ValueError("Email deve ter no máximo 100 caracteres.")
        return value


class RegisterAgapeFamilyFormData(BaseModel):
    endereco: FamilyAddressSchema
    membros: list[FamilyMemberSchema]
    observacao: str | None = Field(None, max_length=255)
    comprovante_residencia: BaseFile | None = None
    fotos_familia: list[BaseFile] | BaseFile | list = []

    @root_validator(pre=True)
    def validate_data(cls, values):
        if "membros" in values and isinstance(values["membros"], str):
            try:
                if not values["membros"].startswith("["):
                    values["membros"] = f"[{values['membros']}]"
                values["membros"] = json.loads(values["membros"])
            except json.JSONDecodeError:
                raise ValueError("O campo 'membros' deve ser um JSON valido.")

        if "endereco" in values and isinstance(values["endereco"], str):
            try:
                values["endereco"] = json.loads(values["endereco"])
            except json.JSONDecodeError:
                raise ValueError("O campo 'endereco' deve ser um JSON valido.")
        return values
