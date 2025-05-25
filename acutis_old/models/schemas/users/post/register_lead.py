from pydantic import BaseModel, EmailStr, Field, constr
from spectree import BaseFile


class RegisterLeadFormData(BaseModel):
    nome: constr(strip_whitespace=True, min_length=3, max_length=100)  # type: ignore
    email: EmailStr = Field(..., description="Email do lead")
    telefone: str = Field(
        ...,
        min_length=11,
        max_length=15,
        description="Celular ou telefone do lead",
    )
    origem: int = Field(..., description="ID da ação de origem do lead")
    intencao: str | None = Field(None, description="Intenção do lead")
    foto: BaseFile | None = Field(None, description="Foto do lead")
