from datetime import date
from typing import Optional
from pydantic import BaseModel, Field
from sqlalchemy import desc


class RegistrarCadastroVocacionalRequest(BaseModel):
    fk_usuario_vocacional_id: int = Field(..., description="Id usuário vocacional")
    documento_identidade: str = Field(
        ..., description="Número de identificação pessoal"
    )
    data_nascimento: date = Field(..., description="Data de nascimento")
    cep: Optional[str] = Field(
        None, description="Cep para brasileiro ou zip_code caso estrangeiro"
    )
    detalhe_estrangeiro: Optional[str] = Field(
        None, description="Detalhes do endereço estrangeiro"
    )
    rua: Optional[str] = Field(None, description="Rua")
    numero: Optional[str] = Field(None, description="Número da residência")
    complemento: Optional[str] = Field(None, description="Complemento residêncial")
    bairro: Optional[str] = Field(None, description="Bairro")
    cidade: Optional[str] = Field(None, description="Cidade onde reside")
    estado: Optional[str] = Field(
        None, description="Estado onde reside", min_length=2, max_length=2
    )
