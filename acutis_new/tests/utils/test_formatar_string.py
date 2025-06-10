import pytest

from acutis_api.application.utils.funcoes_auxiliares import formatar_string


def test_formatar_string_none():
    with pytest.raises(TypeError):
        formatar_string(None)


def test_formatar_string_com_acentos_e_sinais():
    entrada = 'João_ça! É incrível: até amanhã.'
    esperado = 'Joao ca e incrivel ate amanha'
    assert formatar_string(entrada) == esperado


def test_formatar_string_sem_acentos():
    entrada = 'Texto sem acento ou sinais'
    assert formatar_string(entrada) == entrada


def test_formatar_string_com_pontuacoes():
    entrada = 'Olá, mundo! Isso é uma frase...'
    esperado = 'Ola mundo Isso e uma frase'
    assert formatar_string(entrada) == esperado


def test_formatar_string_com_todos_acentos():
    entrada = 'áàãâä éèêë íìîï óòõôö úùûü'
    esperado = 'aaaaa eeee iiii ooooo uuuu'
    assert formatar_string(entrada) == esperado
