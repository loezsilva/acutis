import uuid
from datetime import date, datetime

from pydantic import BaseModel

from acutis_api.domain.repositories.enums import TipoOrdenacaoEnum
from acutis_api.domain.repositories.schemas.paginacao import PaginacaoQuery


class BuscarCardsDoacoesBenfeitoresSchema(BaseModel):
    total_benfeitores: int
    percentual_benfeitores: float
    total_doacoes_anonimas: int
    percentual_quantidade_doacoes: float
    total_montante_anonimo: float
    percentual_total_valor: float
    ticket_medio_anonimo: float
    percentual_ticket_medio: float


class ListarBenfeitoresFiltros(PaginacaoQuery):
    id: uuid.UUID | None = None
    nome_documento: str | None = None
    registrado_em_inicio: date | None = None
    registrado_em_fim: date = datetime.now().date()
    ultima_doacao_inicio: date | None = None
    ultima_doacao_fim: date = datetime.now().date()
    campanha_id: uuid.UUID | None = None
    somente_membros: bool = False
    ordenar_por: str = 'registrado_em'
    tipo_ordenacao: TipoOrdenacaoEnum = TipoOrdenacaoEnum.decrescente


class ListarBenfeitoresSchema(BaseModel):
    id: uuid.UUID
    nome: str
    numero_documento: str
    registrado_em: datetime
    quantidade_doacoes: int
    montante_total: float
    ultima_doacao: datetime


class BuscarInformacoesBenfeitorSchema(BaseModel):
    id: uuid.UUID
    nome: str
    numero_documento: str
    registrado_em: datetime | None
    total_doacoes: int
    total_valor_doado: float
    ultima_doacao: datetime | None


class ListarDoacoesAnonimasBenfeitorSchema(BaseModel):
    criado_em: datetime
    valor: float
