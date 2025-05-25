from pydantic import BaseModel, EmailStr, Field


class UpdateUserByIdRequest(BaseModel):
    pais: str = Field(..., min_length=3, max_length=50, description="Nome do país")
    nome: str = Field(..., min_length=6, max_length=100, description="Nome completo")
    telefone: str = Field(
        min_length=11, max_length=15, description="Celular ou telefone do benfeitor"
    )
    email: EmailStr = Field(..., description="Email do usuário")
