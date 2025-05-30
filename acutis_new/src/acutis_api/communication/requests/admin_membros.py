import uuid
from datetime import date, datetime

from pydantic import field_validator

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
    filtro_dinamico: str | None = None

    @field_validator('filtro_dinamico')
    @classmethod
    def filtro_minimo_quatro_caracteres(cls, value):
        if value is not None and len(value.strip()) < 4:
            raise ValueError(
                'O filtro dinâmico deve ter pelo menos 4 caracteres.'
            )
        return value
