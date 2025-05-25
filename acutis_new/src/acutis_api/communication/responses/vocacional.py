from typing import List
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from acutis_api.communication.enums.vocacional import (
    PassosVocacionalEnum,
    PassosVocacionalStatusEnum,
)
from acutis_api.communication.schemas.vocacional import (
    ListarDesistenciasVocacionaisSchema,
    ListarVocacionaisRecusadosSchema,
    ListarVocacionalSchema,
)


class ListarPreCadastrosResponse(BaseModel):
    pre_cadastros: list[ListarVocacionalSchema]
    pagina: int
    total: int


class ListarCadastrosVocacionaisResponse(BaseModel):
    cadastros_vocacionais: List[ListarVocacionalSchema]
    pagina: int
    total: int


class ListarFichasVocacionaisResponse(BaseModel):
    fichas_vocacionais: List[ListarVocacionalSchema]
    pagina: int
    total: int


class ListarDesistenciasVocacionaisResponse(BaseModel):
    desistencias: list[ListarDesistenciasVocacionaisSchema]
    total: int
    pagina: int


class ListarVocacionaisRecusadosResponse(BaseModel):
    recusados: list[ListarVocacionaisRecusadosSchema]
    total: int
    pagina: int


class DecodificarTokenVocacionalResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    nome: str = Field(..., description='Nome vocacional')
    email: str = Field(..., description='Email vocacional')
    etapa: PassosVocacionalEnum = Field(..., description='Etapa vocacional')
    status: PassosVocacionalStatusEnum = Field(
        ..., description='Status etapa vocacional'
    )
    telefone: str = Field(..., description='Telefonde do vocacional')
    pais: str = Field(..., description='País vocacional')
    fk_usuario_vocacional_id: UUID = Field(..., description='ID vocacional')
