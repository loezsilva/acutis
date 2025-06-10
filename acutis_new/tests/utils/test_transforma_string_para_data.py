from datetime import datetime

from acutis_api.application.utils.funcoes_auxiliares import (
    transforma_string_para_data,
)


def test_data_valida_em_formato_rfc1123():
    data_str = 'Wed, 04 Jun 2025 12:30:00 GMT'
    resultado = transforma_string_para_data(data_str)
    assert isinstance(resultado, datetime)
    assert resultado == datetime(2025, 6, 4, 12, 30, 0)


def test_data_invalida():
    resultado = transforma_string_para_data('04-06-2025')
    assert resultado is None


def test_valor_none():
    resultado = transforma_string_para_data(None)
    assert resultado is None


def test_valor_vazio():
    resultado = transforma_string_para_data('')
    assert resultado is None


def test_valor_numero():
    resultado = transforma_string_para_data(123456)
    assert resultado is None
