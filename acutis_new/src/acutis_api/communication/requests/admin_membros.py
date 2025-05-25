import uuid
from datetime import date, datetime

from acutis_api.communication.enums import TipoOrdenacaoEnum
from acutis_api.communication.enums.admin_membros import (
    ListarLeadsMembrosOrdenarPorEnum,
)
from acutis_api.communication.enums.membros import (
    TipoCadastroEnum,
)
from acutis_api.communication.requests.paginacao import PaginacaoQuery


class ListarLeadsMembrosQuery(PaginacaoQuery):
    nome_email_documento: str = ''
    telefone: str = ''
    tipo_cadastro: TipoCadastroEnum | None = None
    campanha_origem: uuid.UUID | None = None
    data_cadastro_inicial: date | None = None
    data_cadastro_final: date = datetime.now().date()
    ultimo_acesso_inicial: date | None = None
    ultimo_acesso_final: date = datetime.now().date()
    status: bool | None = None
    ordenar_por: ListarLeadsMembrosOrdenarPorEnum = (
        ListarLeadsMembrosOrdenarPorEnum.data_cadastro_lead
    )
    tipo_ordenacao: TipoOrdenacaoEnum = TipoOrdenacaoEnum.decrescente
