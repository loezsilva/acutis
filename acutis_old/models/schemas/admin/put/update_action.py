from typing import Optional
from pydantic import BaseModel, Field
from spectree import BaseFile


class UpdateActionRequest(BaseModel):
    nome: str = Field(..., min_length=3)
    titulo: str = Field(..., min_length=3)
    descricao: str = Field(..., min_length=3)
    status: bool = Field(...)
    preenchimento_foto: bool = Field(...)
    label_foto: Optional[str] = Field(None, min_length=3)


class UpdateActionFormData(BaseModel):
    data: str = Field(...)
    banner: Optional[BaseFile]
    background: Optional[BaseFile]
