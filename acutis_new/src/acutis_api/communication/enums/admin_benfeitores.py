from enum import Enum


class ListarBenfeitoresOrdenarPorEnum(str, Enum):
    id = 'id'
    nome = 'nome'
    numero_documento = 'numero_documento'
    registrado_em = 'registrado_em'
    quantidade_doacoes = 'quantidade_doacoes'
    montante_total = 'montante_total'
    ultima_doacao = 'ultima_doacao'
