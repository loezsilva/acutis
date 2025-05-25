from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class StatusOficialEnum(str, Enum):
    aprovado = 'aprovado'
    pendente = 'pendente'
    recusado = 'recusado'


class AdminAcaoMembroOficialEnum(str, Enum):
    aprovar = 'aprovar'
    recusar = 'recusar'


class ListarMembrosOficiaisSchema(BaseModel):
    nome: Optional[str] = Field(None, description='Nome do membro oficial')
    email: Optional[str] = Field(None, description='Email do membro oficial')
    data_inicial: Optional[str] = Field(None, description='Data inicial')
    data_final: Optional[str] = Field(None, description='Data final')
    fk_cargo_oficial_id: Optional[int] = Field(
        None, description='ID cargo oficial'
    )
    numero_documento: Optional[str] = Field(
        None, description='Número do documento'
    )
    sexo: Optional[str] = Field(None, description='Sexo')
    status: Optional[StatusOficialEnum] = Field(
        None, description='Status do oficial'
    )
    fk_superior_id: Optional[str] = Field(None, description='ID de superior')


class AlterarCargoOficialSchema(BaseModel):
    fk_cargo_oficial_id: str = Field(..., description='ID de cargo oficial')
    fk_membro_oficial: str = Field(..., description='ID de membro oficial')


class AlterarVinculoOficialSchema(BaseModel):
    fk_membro_oficial_id: str = Field(..., description='ID de Membro Oficial')
    fk_membro_superior_oficial_id: str = Field(
        ..., description='ID de Membro Oficial Superior'
    )
