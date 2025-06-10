from datetime import date, timedelta

import pytest

from acutis_api.application.utils.funcoes_auxiliares import calcular_idade


def test_calcular_idade_com_data_date():
    nascimento = date(2000, 1, 1)
    idade_esperada = date.today().year - 2000
    if (date.today().month, date.today().day) < (1, 1):
        idade_esperada -= 1

    assert calcular_idade(nascimento) == idade_esperada


def test_calcular_idade_com_data_string():
    nascimento_str = '2000-01-01'
    idade_esperada = date.today().year - 2000
    if (date.today().month, date.today().day) < (1, 1):
        idade_esperada -= 1

    assert calcular_idade(nascimento_str) == idade_esperada


def test_calcular_idade_com_formato_personalizado():
    nascimento_str = '01/01/2000'
    idade_esperada = date.today().year - 2000
    if (date.today().month, date.today().day) < (1, 1):
        idade_esperada -= 1

    assert calcular_idade(nascimento_str, formato='%d/%m/%Y') == idade_esperada


def test_calcular_idade_com_data_invalida():
    with pytest.raises(ValueError, match=r'Data inválida'):
        calcular_idade('2000-31-01')  # data inválida


def test_calcular_idade_com_data_no_futuro():
    data_futura = date.today() + timedelta(days=1)
    with pytest.raises(
        ValueError, match='data de nascimento não pode estar no futuro'
    ):
        calcular_idade(data_futura)
