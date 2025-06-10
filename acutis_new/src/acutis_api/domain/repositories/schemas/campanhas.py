from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from acutis_api.communication.enums import TipoOrdenacaoEnum
from acutis_api.communication.enums.admin_campanhas import (
    ListarCampanhasOrdenarPorEnum,
)


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
    filtro_dinamico: Optional[str] = None
    ordenar_por: ListarCampanhasOrdenarPorEnum = (
        ListarCampanhasOrdenarPorEnum.criado_em
    )
    tipo_ordenacao: TipoOrdenacaoEnum = TipoOrdenacaoEnum.decrescente


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


class ListarCadastrosCampanhaSchema(BaseModel):
    id: str
    nome: str
    email: str
    telefone: str
    data_cadastro: datetime
