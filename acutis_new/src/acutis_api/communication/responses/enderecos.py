from pydantic import BaseModel


class BuscarCEPResponse(BaseModel):
    bairro: str | None
    cep: str | None
    cidade: str | None
    estado: str | None
    rua: str | None
    tipo_logradouro: str | None
