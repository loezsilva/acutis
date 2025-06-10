from acutis_api.application.utils.funcoes_auxiliares import valida_email


def test_email_vazio():
    valido, msg = valida_email(
        '', verificar_entregabilidade=False, verificar_dominio=False
    )
    assert not valido
    assert msg == 'Você deve inserir um email.'


def test_email_invalido():
    valido, msg = valida_email(
        'email-invalido',
        verificar_entregabilidade=False,
        verificar_dominio=False,
    )
    assert not valido
    assert msg == 'O email inserido é inválido.'


def test_email_valido_sem_verificar_dominio():
    valido, resultado = valida_email(
        'teste@exemplo.com',
        verificar_entregabilidade=False,
        verificar_dominio=False,
    )
    assert valido
    assert resultado == 'teste@exemplo.com'


def test_email_valido_com_dominio_na_lista():
    valido, resultado = valida_email(
        'teste@gmail.com',
        verificar_entregabilidade=False,
        verificar_dominio=True,
    )
    assert valido
    assert resultado == 'teste@gmail.com'


def test_email_valido_com_dominio_fora_da_lista():
    valido, msg = valida_email(
        'teste@dominio.com',
        verificar_entregabilidade=False,
        verificar_dominio=True,
    )
    assert not valido
    assert msg == 'O domínio do email inserido não é permitido.'
