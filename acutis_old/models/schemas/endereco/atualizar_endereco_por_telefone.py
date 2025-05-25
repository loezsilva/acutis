from typing import Optional
from pydantic import BaseModel


class AtualizarEnderecoPorTelefoneRequest(BaseModel):
    telefone: str
    rua: Optional[str]
    numero: Optional[str]
    complemento: Optional[str]
    bairro: Optional[str]
    cidade: Optional[str]
    cep: Optional[str]
    estado: Optional[str]
    detalhe_estrangeiro: Optional[str]

    class Config:
        anystr_strip_whitespace = True
        
    
    
