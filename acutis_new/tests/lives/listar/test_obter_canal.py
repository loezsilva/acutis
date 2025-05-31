from http import HTTPStatus
from unittest.mock import patch

from flask.testing import FlaskClient

LISTAR_CANAIS_ENDPOINT = '/api/admin/lives/obter-canal'


def test_listar_canais_sucesso(
    client: FlaskClient, seed_registrar_canal, membro_token
):
    response = client.get(
        LISTAR_CANAIS_ENDPOINT,
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK

    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert 'id' in data[0]
    assert 'tag' in data[0]
    assert 'rede_social' in data[0]


def test_listar_canais_nao_encontrado(client: FlaskClient, membro_token):
    patch_target = (
        'acutis_api.infrastructure.repositories.lives.'
        'LivesRepository.obter_canal'
    )

    with patch(patch_target) as mock_obter_canal:
        mock_obter_canal.return_value = []

        response = client.get(
            f'{LISTAR_CANAIS_ENDPOINT}?rede_social=inexistente',
            headers={'Authorization': f'Bearer {membro_token}'},
        )

        assert response.status_code == HTTPStatus.NOT_FOUND
        data = response.get_json()
        assert 'msg' in data[0]
        assert 'Não foram encontrados canais cadastrados.' in data[0]['msg']


def test_listar_canais_sem_autenticacao(client: FlaskClient):
    response = client.get(LISTAR_CANAIS_ENDPOINT)
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_listar_canais_filtrado_por_tag(
    client: FlaskClient, seed_registrar_canal, membro_token
):
    response = client.get(
        f'{LISTAR_CANAIS_ENDPOINT}?tag=teste-invalida',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    data = response.get_json()
    assert isinstance(data, list)


def test_listar_canais_filtrado_por_rede_social(
    client: FlaskClient, seed_registrar_canal, membro_token
):
    response = client.get(
        f'{LISTAR_CANAIS_ENDPOINT}?rede_social=youtube',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    data = response.get_json()
    assert isinstance(data, list)
