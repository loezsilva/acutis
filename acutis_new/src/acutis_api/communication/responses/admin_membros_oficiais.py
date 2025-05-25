from typing import Optional

from pydantic import BaseModel


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


class ListarMembrosOficiaisResponse(BaseModel):
    total: int
    pagina: int
    por_pagina: int
    membros_oficiais: list[MembrosOficiaisResponse]
