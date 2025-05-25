import uuid
from typing import Optional

from pydantic import BaseModel, Field

from acutis_api.communication.enums.membros_oficiais import (
    AdminAcaoMembroOficialEnum,
    StatusOficialEnum,
)


class ListarMembrosOficiaisRequest(BaseModel):
    nome: Optional[str] = Field(None, description='Nome do membro oficial')
    email: Optional[str] = Field(None, description='Email do membro oficial')
    data_inicial: Optional[str] = Field(
        None, description='Data inicial (Y-m-d)'
    )
    data_final: Optional[str] = Field(None, description='Data final (Y-m-d)')
    fk_cargo_oficial_id: Optional[uuid.UUID] = Field(
        None, description='ID cargo oficial'
    )
    numero_documento: Optional[str] = Field(
        None, description='Número do documento'
    )
    sexo: Optional[str] = Field(None, description='Sexo')
    status: Optional[StatusOficialEnum] = Field(
        None, description='Status do oficial'
    )
    fk_superior_id: Optional[uuid.UUID] = Field(
        None, description='ID de superior'
    )
    pagina: Optional[int] = Field(default=1, description='Página atual')
    por_pagina: Optional[int] = Field(
        default=10, description='Quantidade por página'
    )
    ordenar_por: Optional[str] = Field(
        default='desc', description='desc | asc'
    )


class AlterarStatusMembroOficialRequest(BaseModel):
    acao: AdminAcaoMembroOficialEnum = Field(
        ..., description=' reprovar | aprovar'
    )

    fk_membro_oficial_id: uuid.UUID = Field(
        ..., description='ID de membro oficial'
    )


class AlterarCargoOficialRequest(BaseModel):
    fk_cargo_oficial_id: uuid.UUID = Field(
        ..., description='ID de cargo oficial'
    )
    fk_membro_oficial: uuid.UUID = Field(
        ..., description='ID de membro oficial'
    )


class AlterarVinculoOficialRequest(BaseModel):
    fk_membro_oficial_id: uuid.UUID = Field(
        ..., description='ID de Membro Oficial'
    )
    fk_membro_superior_oficial_id: uuid.UUID = Field(
        ..., description='ID de Membro Oficial Superior'
    )
