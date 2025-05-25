from enum import Enum


class GeneroVocacionalEnum(str, Enum):
    masculino = 'masculino'
    feminino = 'feminino'


class PassosVocacionalEnum(str, Enum):
    pre_cadastro = 'pre_cadastro'
    cadastro = 'cadastro'
    ficha_vocacional = 'ficha_vocacional'


class PassosVocacionalStatusEnum(str, Enum):
    pendente = 'pendente'
    aprovado = 'aprovado'
    reprovado = 'reprovado'
    desistencia = 'desistencia'


class EstadoCivilEnum(str, Enum):
    casado = 'Casado(a)'
    solteiro = 'Solteiro(a)'
    divorciado = 'Divorciado(a)'
    viuvo = 'Viúvo(a)'
    uniaoestavel = 'União Estável'


class AprovacaoEnum(str, Enum):
    aprovar = 'aprovar'
    reprovar = 'reprovar'
