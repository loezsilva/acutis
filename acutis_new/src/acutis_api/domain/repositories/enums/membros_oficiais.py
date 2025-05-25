from enum import Enum


class StatusMembroOficialEnum(str, Enum):
    aprovado = 'aprovado'
    pendente = 'pendente'
    recusado = 'recusado'
