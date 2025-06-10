from http import HTTPStatus

from flask.testing import FlaskClient

STATUS_PERMISSAO_ENDPOINT = '/api/agape/status-permissao-voluntarios'


def test_listar_status_permissao_voluntarios_sucesso(
    client: FlaskClient, membro_token, seed_menu_agape_e_permissoes
):
    resposta = client.get(
        STATUS_PERMISSAO_ENDPOINT,
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    resposta_json = resposta.json
    assert resposta.status_code == HTTPStatus.OK
    assert 'acessar' in resposta_json
    assert 'criar' in resposta_json
    assert 'editar' in resposta_json
    assert 'deletar' in resposta_json


def test_listar_status_permissao_voluntarios_sem_perfil_cadastrado(
    client: FlaskClient, membro_token
):
    resposta = client.get(
        STATUS_PERMISSAO_ENDPOINT,
        headers={'Authorization': f'Bearer {membro_token}'},
    )
    assert resposta.status_code == HTTPStatus.NOT_FOUND


def test_listar_status_permissao_voluntarios_sem_token(client: FlaskClient):
    resposta = client.get(
        STATUS_PERMISSAO_ENDPOINT,
    )
    assert resposta.status_code == HTTPStatus.UNAUTHORIZED
