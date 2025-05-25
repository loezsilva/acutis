from datetime import date
from uuid import UUID

from pydantic import BaseModel

from acutis_api.domain.entities.usuario_vocacional import GeneroVocacionalEnum
from acutis_api.domain.repositories.enums.vocacional import (
    PassosVocacionalEnum,
    PassosVocacionalStatusEnum,
)


class RegistrarPreCadastroSchema(BaseModel):
    nome: str
    email: str
    telefone: str
    genero: GeneroVocacionalEnum
    pais: str


class RegistrarCadastroVocacionalSchema(BaseModel):
    fk_usuario_vocacional_id: UUID
    documento_identidade: str
    data_nascimento: date
    cep: str | None
    logradouro: str | None
    numero: str | None
    complemento: str | None
    bairro: str | None
    cidade: str | None
    estado: str | None


class ListarPreCadastrosSchema(BaseModel):
    pagina: int | None
    por_pagina: int | None
    pais: str | None
    telefone: str | None
    status: PassosVocacionalStatusEnum | None
    nome: str | None
    email: str | None
    data_inicial: str | None
    data_final: str | None


class ListarCadastrosVocacionaisSchema(BaseModel):
    pagina: int | None
    por_pagina: int | None
    documento_identidade: str | None
    email: str | None
    nome: str | None
    status: PassosVocacionalStatusEnum | None
    genero: GeneroVocacionalEnum | None
    pais: str | None
    telefone: str | None
    data_inicial: str | None
    data_final: str | None


class ListarFichasVocacionaisSchema(BaseModel):
    pagina: int | None
    por_pagina: int | None
    pais: str | None
    status: PassosVocacionalStatusEnum | None
    genero: GeneroVocacionalEnum | None
    email: str | None
    nome: str | None
    documento_identidade: str | None
    data_inicial: str | None
    data_final: str | None
    fk_usuario_vocacional_id: UUID | None
    telefone: str | None


class ListarDesistenciaVocacionaisSchema(BaseModel):
    pagina: int | None
    por_pagina: int | None
    fk_usuario_vocacional_id: UUID | None
    nome: str | None
    email: str | None
    desistencia_em: str | None
    etapa: str | None
    pais: str | None
    telefone: str | None
    genero: GeneroVocacionalEnum | None
    documento_identidade: str | None
    data_inicial: str | None
    data_final: str | None


class ListarVocacionaisRecusadosSchema(BaseModel):
    pagina: int | None
    por_pagina: int | None
    data_inicial: str | None
    data_final: str | None
    nome: str | None
    email: str | None
    etapa: str | None
    pais: str | None
    pais: str | None
    telefone: str | None
    genero: str | None
    status: str | None
    documento_identidade: str | None


class DecodificarTokenVocacionalSchema(BaseModel):
    nome: str
    email: str
    etapa: PassosVocacionalEnum
    status: PassosVocacionalStatusEnum
    telefone: str
    pais: str
    fk_usuario_vocacional_id: UUID
