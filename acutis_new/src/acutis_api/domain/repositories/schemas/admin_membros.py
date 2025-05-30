import uuid
from datetime import date, datetime

from pydantic import BaseModel

from acutis_api.domain.entities.membro import SexoEnum
from acutis_api.domain.repositories.enums import TipoOrdenacaoEnum
from acutis_api.domain.repositories.enums.admin_membros import (
    TipoCadastroEnum,
)
from acutis_api.domain.repositories.schemas.paginacao import PaginacaoQuery


class ListarLeadsMembrosFiltros(PaginacaoQuery):
    nome_email_documento: str = ''
    telefone: str = ''
    tipo_cadastro: TipoCadastroEnum | None = None
    campanha_origem: uuid.UUID | None = None
    data_cadastro_inicial: date | None = None
    data_cadastro_final: date = datetime.now().date()
    ultimo_acesso_inicial: date | None = None
    ultimo_acesso_final: date = datetime.now().date()
    status: bool | None = None
    ordenar_por: str = 'data_cadastro_lead'
    tipo_ordenacao: TipoOrdenacaoEnum = TipoOrdenacaoEnum.decrescente
    filtro_dinamico: str | None = None


class ListarLeadsMembrosSchema(BaseModel):
    lead_id: uuid.UUID
    nome: str
    email: str
    telefone: str | None
    pais: str | None
    data_cadastro_lead: str
    lead_atualizado_em: str
    membro_id: uuid.UUID | None
    benfeitor_id: uuid.UUID | None
    endereco_id: uuid.UUID | None
    nome_social: str | None
    data_nascimento: str | None
    numero_documento: str | None
    sexo: SexoEnum | None
    foto: str | None
    ultimo_acesso: str | None
    status_conta_lead: bool | None
    data_cadastro_membro: str | None
    membro_atualizado_em: str | None
    cadastro_membro_atualizado_em: str | None
