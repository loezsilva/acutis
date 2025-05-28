import uuid
from datetime import date, datetime

from acutis_api.communication.enums import TipoOrdenacaoEnum
from acutis_api.communication.enums.admin_benfeitores import (
    ListarBenfeitoresOrdenarPorEnum,
)
from acutis_api.communication.requests.paginacao import PaginacaoQuery


class ListarBenfeitoresQuery(PaginacaoQuery):
    id: uuid.UUID | None = None
    nome_documento: str | None = None
    registrado_em_inicio: date | None = None
    registrado_em_fim: date = datetime.now().date()
    ultima_doacao_inicio: date | None = None
    ultima_doacao_fim: date = datetime.now().date()
    campanha_id: uuid.UUID | None = None
    somente_membros: bool = False
    ordenar_por: ListarBenfeitoresOrdenarPorEnum = (
        ListarBenfeitoresOrdenarPorEnum.registrado_em
    )
    tipo_ordenacao: TipoOrdenacaoEnum = TipoOrdenacaoEnum.decrescente
