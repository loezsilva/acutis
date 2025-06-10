import uuid
from typing import Optional

from pydantic import BaseModel, Field, field_validator

from acutis_api.communication.enums import TipoOrdenacaoEnum
from acutis_api.communication.enums.admin_membros_oficiais import (
    ListarMembrosOficiaisOrdenarPorEnum,
)
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
    ordenar_por: ListarMembrosOficiaisOrdenarPorEnum = (
        ListarMembrosOficiaisOrdenarPorEnum.criado_em
    )
    tipo_ordenacao: TipoOrdenacaoEnum = TipoOrdenacaoEnum.decrescente
    filtro_dinamico: Optional[str] = Field(None, description='Filtro dinâmico')

    @field_validator('filtro_dinamico')
    @classmethod
    def filtro_minimo_quatro_caracteres(cls, value):
        if value is not None and len(value.strip()) < 4:
            raise ValueError(
                'O filtro dinâmico deve ter pelo menos 4 caracteres.'
            )
        return value


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
