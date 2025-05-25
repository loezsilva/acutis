from typing import Optional
from pydantic import BaseModel, Field


class RegisterProfileRequest(BaseModel):
    nome: str = Field(..., min_length=3, max_length=45)
    status: Optional[bool] = Field(
        description="Define se o perfil será criado com status ativo ou inativo. (Se não passado nenhum valor, será criado como inativo.)"
    )
    super_perfil: bool = Field(
        description="Define se o perfil terá acesso ao painel do administrador."
    )
