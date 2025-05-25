from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class ConfirmSelectedLeadQuery(BaseModel):
    sobrepor_sorteio: bool = Field(
        False, description="Define se deseja sobrepor um lead já sorteado"
    )


class ConfirmSelectedLeadRequest(BaseModel):
    nome: str = Field(..., description="Nome do lead sorteado")
    email: EmailStr = Field(..., description="Email do lead sorteado")
    acao_id: int = Field(..., description="ID da ação que ocorreu o sorteio")
    lead_sorteado_id: Optional[int] = Field(
        None,
        description="ID do lead sorteado anteriormente para ser sobrescrito. (Esse campo é obrigatório caso o ```sobrepor_sorteio``` seja ```True```)",
    )
