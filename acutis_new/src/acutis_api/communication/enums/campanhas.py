from enum import Enum


class ObjetivosCampanhaEnum(str, Enum):
    pre_cadastro = 'pre_cadastro'
    cadastro = 'cadastro'
    doacao = 'doacao'
    oficiais = 'oficiais'


class TiposCampoEnum(str, Enum):
    string = 'string'
    integer = 'int'
    float = 'float'
    date = 'date'
    datetime = 'datetime'
    arquivo = 'arquivo'
    imagem = 'imagem'
