import pytest

from acutis_api.application.utils.funcoes_auxiliares import valida_cpf_cnpj
from acutis_api.exception.errors_handler import HttpBadRequestError


def test_valida_cpf_cnpj():
    assert valida_cpf_cnpj('123452', 'testes') == '123452'


def test_valida_cpf_cnpj_cpf_invalido():
    with pytest.raises(HttpBadRequestError) as exc_info:
        valida_cpf_cnpj('12345678901', 'cpf')
    assert str(exc_info.value) == 'CPF inválido!'


def test_valida_cpf_cnpj_cnpj_invalido():
    with pytest.raises(HttpBadRequestError) as exc_info:
        valida_cpf_cnpj('12345678901234', 'cnpj')

    assert str(exc_info.value) == 'CNPJ inválido!'
