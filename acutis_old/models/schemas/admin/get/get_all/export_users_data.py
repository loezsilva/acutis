from typing import Optional

from pydantic import BaseModel


class ExportUsersDataCSV(BaseModel):
    id: int
    pais: Optional[str]
    nome: Optional[str]
    nome_social: Optional[str]
    numero_documento: Optional[str]
    email: Optional[str]
    telefone: Optional[str]
    data_nascimento: Optional[str]
    sexo: Optional[str]
    estado: Optional[str]
    cidade: Optional[str]
    cep: Optional[str]
    bairro: Optional[str]
    rua: Optional[str]
    numero: Optional[str]
    complemento: Optional[str]

    class Config:
        orm_mode = True
