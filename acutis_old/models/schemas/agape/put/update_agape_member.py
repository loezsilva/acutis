from datetime import date
from pydantic import BaseModel, EmailStr, Field, constr, validator
from spectree import BaseFile


class UpdateAgapeMemberFormData(BaseModel):
    responsavel: bool
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
    foto_documento: BaseFile | None = None

    @validator("email")
    def check_email_length(cls, value):
        if value and len(value) > 100:
            raise ValueError("Email deve ter no máximo 100 caracteres.")
        return value
