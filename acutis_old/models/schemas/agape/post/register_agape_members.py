from datetime import date
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field, constr, validator


class AgapeMemberSchema(BaseModel):
    responsavel: Optional[bool] = False
    nome: constr(min_length=3, max_length=100, strip_whitespace=True)  # type: ignore
    email: Optional[EmailStr]
    telefone: Optional[str] = Field(None, max_length=20)
    cpf: Optional[str] = Field(None, max_length=14)
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


class RegisterAgapeMembersRequest(BaseModel):
    membros: List[AgapeMemberSchema]
