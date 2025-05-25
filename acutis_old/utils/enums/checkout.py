from enum import Enum


class Status(str, Enum):
    em_processamento = 0,
    pago = 1,
    nao_efetuado = 2,
    expirado = 3


class TipoPagamento(str, Enum):
    cartao_credito = 1,
    pix = 2,
    boleto = 3


class TipoPagamentoMP(str, Enum):
    pix = 'pix'
    boleto = 'bolbradesco'
