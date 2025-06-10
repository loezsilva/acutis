import uuid
from datetime import date, timedelta
from http import HTTPStatus
from unittest.mock import patch

from flask.testing import FlaskClient

LISTAR_AUDIENCIA_LIVES_ENDPOINT = '/api/admin/lives/obter-audiencia-lives'


def test_obter_dados_audiencia_lives_sucesso(
    client: FlaskClient, seed_audiencia_lives, membro_token
):
    audiencia, live = seed_audiencia_lives

    assert live.id is not None

    response = client.get(
        f'{LISTAR_AUDIENCIA_LIVES_ENDPOINT}?live_id={str(live.id)}',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK

    response_data = response.get_json()

    assert isinstance(response_data, list)
    assert len(response_data) > 0
    assert 'titulo' in response_data[0]
    assert 'audiencia' in response_data[0]
    assert 'data_hora' in response_data[0]


def test_obter_dados_audiencia_lives_nenhum_registro(
    client: FlaskClient, seed_registrar_canal, membro_token
):
    live = seed_registrar_canal

    response = client.get(
        f'{LISTAR_AUDIENCIA_LIVES_ENDPOINT}?live_id={str(live.id)}',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert isinstance(response.json, list)
    assert len(response.json) > 0
    assert (
        response.json[0]['msg']
        == 'Nenhuma audiência encontrada para esta live.'
    )


def test_obter_dados_audiencia_lives_live_inexistente(
    client: FlaskClient, membro_token
):
    live_id_invalido = str(uuid.uuid4())

    response = client.get(
        f'{LISTAR_AUDIENCIA_LIVES_ENDPOINT}?live_id={live_id_invalido}',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert isinstance(response.json, list)
    assert len(response.json) > 0
    assert (
        response.json[0]['msg']
        == 'Nenhuma audiência encontrada para esta live.'
    )


def test_obter_dados_audiencia_lives_sem_autenticacao(client: FlaskClient):
    response = client.get(
        f'{LISTAR_AUDIENCIA_LIVES_ENDPOINT}?live_id={str(uuid.uuid4())}'
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_obter_dados_audiencia_lives_sem_parametros(
    client: FlaskClient, membro_token
):
    response = client.get(
        LISTAR_AUDIENCIA_LIVES_ENDPOINT,
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_obter_dados_audiencia_lives_uuid_invalido(
    client: FlaskClient, membro_token
):
    response = client.get(
        f'{LISTAR_AUDIENCIA_LIVES_ENDPOINT}?live_id=abc123',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_obter_dados_audiencia_lives_com_datas(
    client: FlaskClient, seed_audiencia_lives, membro_token
):
    audiencia, live = seed_audiencia_lives

    url = (
        f'{LISTAR_AUDIENCIA_LIVES_ENDPOINT}?live_id={str(live.id)}'
        f'&data_inicial={date.today().replace(day=1).strftime("%Y-%m-%d")}'
        f'&data_final={
            (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")
        }'
    )

    response = client.get(
        url,
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    response_data = response.get_json()
    assert isinstance(response_data, list)


def test_obter_dados_audiencia_lives_erro(client: FlaskClient, membro_token):
    patch_target = (
        'acutis_api.application.use_cases.lives.'
        'listar.obter_audiencia_lives.ObterAudienciaLivesUseCase.execute'
    )

    with patch(patch_target) as mock_execute:
        mock_execute.side_effect = Exception('Erro interno simulado')

        live_id = str(uuid.uuid4())
        response = client.get(
            f'{LISTAR_AUDIENCIA_LIVES_ENDPOINT}?live_id={live_id}',
            headers={'Authorization': f'Bearer {membro_token}'},
        )

        assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
