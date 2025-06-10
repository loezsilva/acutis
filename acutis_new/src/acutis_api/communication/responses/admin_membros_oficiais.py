from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class CampanhasRegistradasSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    nome: str | None
    campos_adicionais: list[dict[str, Any]]


class MembrosOficiaisResponse(BaseModel):
    id: str
    nome: str
    email: str
    cargo_oficial: str
    criado_em: str
    numero_documento: str
    sexo: str
    status: str
    superior: Optional[str]
    foto: Optional[str]

    logradouro: Optional[str]
    numero: Optional[str]
    bairro: Optional[str]
    codigo_postal: Optional[str]
    cidade: Optional[str]
    complemento: Optional[str]
    pais: str
    campanhas_registradas: Optional[list[CampanhasRegistradasSchema]] = None


class ListarMembrosOficiaisResponse(BaseModel):
    total: int
    pagina: int
    por_pagina: int
    membros_oficiais: list[MembrosOficiaisResponse]
