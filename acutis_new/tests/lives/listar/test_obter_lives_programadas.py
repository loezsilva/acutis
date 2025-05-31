from http import HTTPStatus

from flask.testing import FlaskClient

LISTAR_LIVES_PROGRAMADAS_ENDPOINT = '/api/admin/lives/obter-lives-programadas'


def test_obter_lives_programadas_sucesso(
    client: FlaskClient,
    seed_registrar_live_avulsa,
    seed_registrar_live_recorrente,
    membro_token,
):
    _, avulsa = seed_registrar_live_avulsa

    response = client.get(
        LISTAR_LIVES_PROGRAMADAS_ENDPOINT,
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK

    data = response.json
    assert isinstance(data, list)

    tipos = {live['tipo_programacao'] for live in data}
    assert 'avulsa' in tipos
    assert 'recorrente' in tipos


def test_listar_lives_programadas_sem_resultados(
    client: FlaskClient, membro_token
):
    response = client.get(
        LISTAR_LIVES_PROGRAMADAS_ENDPOINT,
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_obter_lives_programadas_filtrado_por_rede_social(
    client: FlaskClient,
    seed_registrar_live_avulsa,
    seed_registrar_live_recorrente,
    membro_token,
):
    response = client.get(
        f'{LISTAR_LIVES_PROGRAMADAS_ENDPOINT}?rede_social=youtube',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    data = response.get_json()
    assert isinstance(data, list)


def test_obter_lives_programadas_filtrado_por_dia_semana(
    client: FlaskClient,
    seed_registrar_live_recorrente,
    membro_token,
):
    url = (
        f'{LISTAR_LIVES_PROGRAMADAS_ENDPOINT}?'
        'filtro_dias_semana[]=segunda-feira'
    )
    response = client.get(
        url,
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    data = response.get_json()
    assert isinstance(data, list)
