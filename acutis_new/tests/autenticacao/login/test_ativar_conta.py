from http import HTTPStatus

from flask.testing import FlaskClient

from acutis_api.application.utils.funcoes_auxiliares import (
    TokenSaltEnum,
    gerar_token,
)

ROTA_ATIVACAO_DE_CONTA = '/api/autenticacao/ativacao-de-conta'


def test_ativar_conta_not_foud(client: FlaskClient):
    token = gerar_token(
        {'email': 'emailnotfound@gmail.com'}, TokenSaltEnum.ativar_conta
    )

    payload = {
        'token': str(token),
        'senha': 'Teste123!',
    }

    response = client.post(
        ROTA_ATIVACAO_DE_CONTA,
        json=payload,
    )

    assert response.status_code == HTTPStatus.NOT_FOUND

    assert response.get_json() == [{'msg': 'Usuário não encontrado'}]


def test_ativar_conta_token_invalido(
    client: FlaskClient, seed_registrar_membro
):
    lead, _, _ = seed_registrar_membro(
        nome='Cleiton ativador de conta', status=True
    )

    token = 'tokeninvalido123'
    payload = {'token': str(token), 'senha': 'Teste123!'}

    response = client.post(
        ROTA_ATIVACAO_DE_CONTA,
        json=payload,
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED

    assert response.get_json() == [{'msg': 'Token inválido.'}]


def test_ativar_conta_ja_ativa(client: FlaskClient, seed_registrar_membro):
    lead, _, _ = seed_registrar_membro(
        nome='Cleiton ativador de conta', status=True
    )

    token = gerar_token({'email': lead.email}, TokenSaltEnum.ativar_conta)

    payload = {'token': str(token), 'senha': 'Teste123!'}

    response = client.post(
        ROTA_ATIVACAO_DE_CONTA,
        json=payload,
    )

    assert response.status_code == HTTPStatus.CONFLICT

    assert response.get_json() == [{'msg': 'Conta já está ativa'}]


def test_ativar_conta_sucesso(client: FlaskClient, seed_registrar_membro):
    lead, _, _ = seed_registrar_membro(nome='Cleiton ativador de conta')

    token = gerar_token({'email': lead.email}, TokenSaltEnum.ativar_conta)

    payload = {'token': str(token), 'senha': 'Teste123!'}

    response = client.post(
        ROTA_ATIVACAO_DE_CONTA,
        json=payload,
    )

    assert response.status_code == HTTPStatus.OK
    assert lead.status == 1


def test_erro_senha_com_espaco_em_branco(
    client: FlaskClient, seed_registrar_membro
):
    lead, _, _ = seed_registrar_membro(nome='Cleiton ativador de conta')
    token = gerar_token({'email': lead.email}, TokenSaltEnum.ativar_conta)

    payload = {'token': str(token), 'senha': 'Teste 123!'}

    response = client.post(
        ROTA_ATIVACAO_DE_CONTA,
        json=payload,
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    assert response.json == [
        {
            'input': 'Teste 123!',
            'loc': ['senha'],
            'msg': 'A senha não pode conter espaços em branco.',
            'type': 'value_error',
        }
    ]


def test_erro_senha_sem_numero(client: FlaskClient, seed_registrar_membro):
    lead, _, _ = seed_registrar_membro(nome='Cleiton ativador de conta')
    token = gerar_token({'email': lead.email}, TokenSaltEnum.ativar_conta)

    payload = {'token': str(token), 'senha': 'Testedasd!'}

    response = client.post(
        ROTA_ATIVACAO_DE_CONTA,
        json=payload,
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    assert response.json == [
        {
            'input': 'Testedasd!',
            'loc': ['senha'],
            'msg': 'A senha deve conter pelo menos um número.',
            'type': 'value_error',
        }
    ]


def test_erro_senha_sem_letra_maiuscula(
    client: FlaskClient, seed_registrar_membro
):
    lead, _, _ = seed_registrar_membro(nome='Cleiton ativador de conta')
    token = gerar_token({'email': lead.email}, TokenSaltEnum.ativar_conta)

    payload = {'token': str(token), 'senha': 'testas12d!'}

    response = client.post(
        ROTA_ATIVACAO_DE_CONTA,
        json=payload,
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    assert response.json == [
        {
            'input': 'testas12d!',
            'loc': ['senha'],
            'msg': 'A senha deve conter pelo menos uma letra maiúscula.',
            'type': 'value_error',
        }
    ]


def test_erro_senha_sem_letra_minuscula(
    client: FlaskClient, seed_registrar_membro
):
    lead, _, _ = seed_registrar_membro(nome='Cleiton ativador de conta')
    token = gerar_token({'email': lead.email}, TokenSaltEnum.ativar_conta)

    payload = {'token': str(token), 'senha': '#TESTE@123'}

    response = client.post(
        ROTA_ATIVACAO_DE_CONTA,
        json=payload,
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    assert response.json == [
        {
            'input': '#TESTE@123',
            'loc': ['senha'],
            'msg': 'A senha deve conter pelo menos uma letra minúscula.',
            'type': 'value_error',
        }
    ]


def test_erro_senha_sem_caracteres_especiais(
    client: FlaskClient, seed_registrar_membro
):
    lead, _, _ = seed_registrar_membro(nome='Cleiton ativador de conta')
    token = gerar_token({'email': lead.email}, TokenSaltEnum.ativar_conta)

    payload = {'token': str(token), 'senha': 'Teste123'}

    response = client.post(
        ROTA_ATIVACAO_DE_CONTA,
        json=payload,
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    assert response.json == [
        {
            'input': 'Teste123',
            'loc': ['senha'],
            'msg': 'A senha deve conter pelo menos um caractere especial.',
            'type': 'value_error',
        }
    ]


def test_verifica_token_ativacao(client: FlaskClient, seed_registrar_membro):
    lead, _, _ = seed_registrar_membro(nome='Cleiton ativador de conta')

    token = gerar_token({'email': lead.email}, TokenSaltEnum.ativar_conta)

    payload = {'token': str(token)}

    response = client.post(
        '/api/autenticacao/verificar-token-ativacao-de-conta',
        json=payload,
    )

    assert response.status_code == HTTPStatus.OK
    assert response.get_json() == {'email': lead.email}


def test_verifica_token_ativao_invalido(client: FlaskClient):
    token = 'tokeninvalido123'
    response = client.post(
        '/api/autenticacao/verificar-token-ativacao-de-conta',
        json={'token': str(token)},
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.get_json() == [{'msg': 'Token inválido.'}]


def test_verifica_token_ativao_email_invalido(client: FlaskClient):
    token = gerar_token(
        {'email': 'cleiton@gmail.com'}, TokenSaltEnum.ativar_conta
    )

    response = client.post(
        '/api/autenticacao/verificar-token-ativacao-de-conta',
        json={'token': str(token)},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.get_json() == [{'msg': 'Usuário não encontrado'}]


def test_verifica_token_ativao_conta_ja_ativa(
    client: FlaskClient, seed_registrar_membro
):
    lead, _, _ = seed_registrar_membro(
        nome='Cleiton ativador de conta',
        status=True,
    )

    token = gerar_token({'email': lead.email}, TokenSaltEnum.ativar_conta)
    payload = {'token': str(token)}

    response = client.post(
        '/api/autenticacao/verificar-token-ativacao-de-conta',
        json=payload,
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.get_json() == [{'msg': 'Conta já está ativa'}]
