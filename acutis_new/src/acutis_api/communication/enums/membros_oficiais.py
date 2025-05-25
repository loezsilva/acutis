from enum import Enum


class StatusOficialEnum(str, Enum):
    aprovado = 'aprovado'
    pendente = 'pendente'
    recusado = 'recusado'


class AdminAcaoMembroOficialEnum(str, Enum):
    aprovar = 'aprovar'
    recusar = 'recusar'
