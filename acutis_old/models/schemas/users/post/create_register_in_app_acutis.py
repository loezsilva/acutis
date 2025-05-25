from enum import Enum
from pydantic import BaseModel, Field

class PatenteEnum(str, Enum):
    patente_1 = "membro"
    patente_2 = "general"
    patente_3 = "marechal"

class CreateRegisterAppAcutis(BaseModel):
    name: str = Field(..., description="Nome do cadastro do usuário")
    email: str = Field(..., description="Email do cadastro do usuário")
    cpf: str = Field(..., description="CPF do cadastro do usuário")
    patent: PatenteEnum = Field(..., description="Patente do usuário")