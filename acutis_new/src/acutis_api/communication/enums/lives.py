from enum import Enum


class TipoProgramacaoLiveEnum(str, Enum):
    AVULSA = 'avulsa'
    RECORRENTE = 'recorrente'


class DiaSemanaEnum(str, Enum):
    SEGUNDA = 'segunda'
    TERCA = 'terça'
    QUARTA = 'quarta'
    QUINTA = 'quinta'
    SEXTA = 'sexta'
    SABADO = 'sábado'
    DOMINGO = 'domingo'

    @classmethod
    def ordem_dias(cls):
        return {
            cls.DOMINGO.value: 1,
            cls.SEGUNDA.value: 2,
            cls.TERCA.value: 3,
            cls.QUARTA.value: 4,
            cls.QUINTA.value: 5,
            cls.SEXTA.value: 6,
            cls.SABADO.value: 7,
        }
