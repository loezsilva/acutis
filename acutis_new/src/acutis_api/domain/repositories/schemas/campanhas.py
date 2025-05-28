from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ListarCampanhasQuery(BaseModel):
    pagina: int
    por_pagina: int
    id: Optional[int]
    nome: Optional[str]
    objetivo: Optional[str]
    publica: Optional[bool]
    ativa: Optional[bool]
    data_inicial: Optional[str]
    data_final: Optional[str]
    ordenar_por: Optional[str]


class RegistrarCampanhaSchema(BaseModel):
    nome: Optional[str]
    objetivo: Optional[str]
    publica: Optional[bool]
    ativa: Optional[bool]
    meta: Optional[str]
    chave_pix: Optional[str]
    foto_campa: Optional[str]
    fk_cargo_oficial_id: Optional[str]
    superior_obrigatorio: bool = False


class RegistrarNovaLandingPageSchema(BaseModel):
    conteudo: Optional[str]
    shlink: Optional[str]


class RegistroNovoCampoAdicionalSchema(BaseModel):
    nome_campo: Optional[str]
    tipo_campo: Optional[str]
    obrigatorio: Optional[bool]


class ListarDoacoesCampanhaSchema(BaseModel):
    valor: float
    data_doacao: datetime
    forma_pagamento: str
    nome: str
