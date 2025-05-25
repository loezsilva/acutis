from http import HTTPStatus

from flask.testing import FlaskClient

ENDPOINT_VERIFICA_CADASTRO_POR_EMAIL = (
    '/api/autenticacao/verificar-cadastro-por-email'
)


def test_verificar_conta_por_email_inativa(
    client: FlaskClient, seed_lead_inativo
):
    email = seed_lead_inativo.email

    response = client.get(
        f'{ENDPOINT_VERIFICA_CADASTRO_POR_EMAIL}/{email}',
    )

    assert response.status_code == HTTPStatus.FORBIDDEN

    assert response.get_json() == [
        {
            'msg': 'Ative sua conta pelo link enviado ao seu e-mail antes de fazer login.'  # noqa
        }
    ]


def test_verificar_conta_por_email_nao_existe(
    client: FlaskClient,
):
    response = client.get(
        f'{ENDPOINT_VERIFICA_CADASTRO_POR_EMAIL}/yandamandioca@gmail.com',
    )

    assert response.status_code == HTTPStatus.NOT_FOUND

    assert response.get_json() == [{'msg': 'Cadastro não encontrado.'}]


def test_verificar_conta_por_email_sucesso(
    client: FlaskClient, seed_lead_ativo
):
    email = seed_lead_ativo.email

    response = client.get(
        f'{ENDPOINT_VERIFICA_CADASTRO_POR_EMAIL}/{email}',
    )

    assert response.status_code == HTTPStatus.OK

    assert response.get_json() == {'msg': 'Cadastro encontrado com sucesso'}
