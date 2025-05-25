from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class DadosPessoais(BaseModel):
    pais: str
    nome: str
    email: str
    cpf: str 
    data_nascimento: datetime
    telefone: str  
    sexo: str  
    password: str
    new_password: str
    agreement: bool
    cep: str  
    rua: str
    numero: str
    bairro: str
    estado: str
    cidade: str
    brasileiro: bool
    fk_empresa_id: int
    fk_landpage_id: Optional[int] = None
    fk_campanha_id: int
    tipo_clifor: str  
    country: str
    campanha_origem: str

class Imagem(BaseModel):
    image: str  

class FormData(BaseModel):
    data: DadosPessoais
    image: Imagem