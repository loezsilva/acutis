from typing import Optional
from pydantic import BaseModel


class AgapeFamilySchema(BaseModel):
    id: int
    nome_familia: str
    observacao: str | None = None
    comprovante_residencia: str | None = None
    cadastrado_em: str
    status: bool
    ultimo_recebimento: Optional[str] = None

    class Config:
        orm_mode = True


class AgapeFamilyAddressSchema(BaseModel):
    cep: str
    rua: str
    numero: Optional[str]
    complemento: Optional[str]
    ponto_referencia: Optional[str]
    bairro: str
    cidade: str
    estado: str

    class Config:
        orm_mode = True


class GetAgapeFamilyByCpfResponse(BaseModel):
    familia: AgapeFamilySchema
    endereco: AgapeFamilyAddressSchema
    fotos_familia: list[str]
