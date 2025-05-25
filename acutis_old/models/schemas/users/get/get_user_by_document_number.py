from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class DocumentTypesEnum(str, Enum):
    CPF = "cpf"
    IDENTIDADE_ESTRANGEIRA = "identidade_estrangeira"


class GetUserByDocumentNumberRequest(BaseModel):
    numero_documento: str = Field(
        ..., min_length=6, max_length=20, description="Número do documento"
    )
    tipo_documento: DocumentTypesEnum


class GetUserByDocumentNumberResponse(BaseModel):
    usuario: bool = Field(
        ..., description="Retorna verdadeiro caso seja usuário cadastrado"
    )
    general: bool = Field(
        ..., description="Retorna verdadeiro caso for general"
    )
    email: Optional[str]
    
class BuscaUsuarioPorContatoOuDocumentoResponse(BaseModel):
    usuario_id = int
