from enum import Enum


class PassosVocacionalEnum(str, Enum):
    pre_cadastro = 'pre_cadastro'
    cadastro = 'cadastro'
    ficha_vocacional = 'ficha_vocacional'


class PassosVocacionalStatusEnum(str, Enum):
    pendente = 'pendente'
    aprovado = 'aprovado'
    reprovado = 'reprovado'
    desistencia = 'desistencia'
