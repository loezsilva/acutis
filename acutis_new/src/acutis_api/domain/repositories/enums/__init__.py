from enum import Enum


class TipoOrdenacaoEnum(str, Enum):
    crescente = 'asc'
    decrescente = 'desc'
