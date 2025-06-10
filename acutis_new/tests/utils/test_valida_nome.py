from acutis_api.application.utils.funcoes_auxiliares import valida_nome


def test_valida_nome_none():
    valido, erro = valida_nome(None)
    assert not valido
    assert erro == 'Você deve inserir um nome.'


def test_valida_nome_valido():
    valido, retorno = valida_nome('Maria Luísa')
    assert valido
    assert retorno == 'Maria Luísa'


def test_valida_nome_valido_com_acentos():
    valido, retorno = valida_nome('João Antônio')
    assert valido
    assert retorno == 'João Antônio'


def test_valida_nome_com_caracteres_invalidos():
    valido, erro = valida_nome('Pedro123')
    assert not valido
    assert erro == 'O nome Pedro123 inserido possui caracteres inválidos.'


def test_valida_nome_com_simbolos():
    valido, erro = valida_nome('Ana!@#')
    assert not valido
    assert erro == 'O nome Ana!@# inserido possui caracteres inválidos.'
