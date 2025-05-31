from http import HTTPStatus
from unittest.mock import patch

from flask.testing import FlaskClient

DADOS_HISTOGRAMA_ENDPOINT = '/api/admin/lives/obter-dados-histograma'


def test_obter_histograma_audiencia_sucesso(
    client: FlaskClient, seed_audiencia_lives, membro_token
):
    audiencia, live = seed_audiencia_lives

    url = (
        f'{DADOS_HISTOGRAMA_ENDPOINT}?filtro_titulo_live={audiencia.titulo}&'
        f'filtro_rede_social={live.rede_social}'
    )

    response = client.get(
        url,
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK

    data = response.get_json()

    assert isinstance(data, dict)
    assert 'audiencia_maxima' in data
    assert 'audiencia_minima' in data
    assert 'audiencia_media' in data
    assert 'canal_principal' in data
    assert 'live_data' in data
    assert isinstance(data['live_data'], list)
    assert len(data['live_data']) > 0
    assert 'titulo' in data['live_data'][0]
    assert 'dados' in data['live_data'][0]
    assert isinstance(data['live_data'][0]['dados'], list)


def test_obter_dados_histograma_nenhum_registro(
    client: FlaskClient, membro_token
):
    payload = {'filtro_titulo_live': 'canal-teste'}

    response = client.get(
        DADOS_HISTOGRAMA_ENDPOINT,
        query_string=payload,
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_obter_histograma_sem_audiencia(
    client: FlaskClient, seed_registrar_canal, membro_token
):
    url = (
        f'{DADOS_HISTOGRAMA_ENDPOINT}?'
        f'filtro_titulo_live={seed_registrar_canal.tag}'
    )

    response = client.get(
        url,
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_obter_histograma_faltando_parametros(
    client: FlaskClient, membro_token
):
    response = client.get(
        DADOS_HISTOGRAMA_ENDPOINT,
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_obter_histograma_rede_social_nao_corresponde(
    client: FlaskClient, seed_audiencia_lives, membro_token
):
    audiencia, _ = seed_audiencia_lives

    url = (
        f'{DADOS_HISTOGRAMA_ENDPOINT}?'
        f'filtro_titulo_live={audiencia.titulo}&'
        f'filtro_rede_social=twitter'
    )

    response = client.get(
        url,
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_obter_dados_histograma_erro_servidor(
    client: FlaskClient, membro_token
):
    patch_target = (
        'acutis_api.application.use_cases.lives.'
        'listar.obter_dados_histograma.'
        'ObterHistogramaLiveUseCase.execute'
    )

    with patch(patch_target) as mock_execute:
        mock_execute.side_effect = Exception('Erro interno')

        response = client.get(
            f'{DADOS_HISTOGRAMA_ENDPOINT}?filtro_titulo_live=teste',
            headers={'Authorization': f'Bearer {membro_token}'},
        )

        assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
