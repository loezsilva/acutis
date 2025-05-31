from http import HTTPStatus
from unittest.mock import patch

from flask.testing import FlaskClient

OBTER_DATAS_LIVES_OCORRIDAS_ENDPOINT = (
    '/api/admin/lives/obter-datas-lives-ocorridas'
)


def test_obter_datas_lives_ocorridas_sucesso(
    client: FlaskClient, seed_audiencia_lives, membro_token
):
    response = client.get(
        OBTER_DATAS_LIVES_OCORRIDAS_ENDPOINT,
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK

    data = response.get_json()

    assert 'datas' in data

    assert isinstance(data['datas'], list)
    assert len(data['datas']) > 0

    for date_str in data['datas']:
        assert len(date_str) == 10
        assert date_str[4] == '-'
        assert date_str[7] == '-'


def test_obter_datas_lives_ocorridas_sem_datas(
    client: FlaskClient, membro_token
):
    response = client.get(
        OBTER_DATAS_LIVES_OCORRIDAS_ENDPOINT,
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_obter_datas_lives_ocorridas_erro(client: FlaskClient, membro_token):
    response = client.get(
        OBTER_DATAS_LIVES_OCORRIDAS_ENDPOINT,
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_obter_datas_lives_ocorridas_faltando_token(client: FlaskClient):
    response = client.get(OBTER_DATAS_LIVES_OCORRIDAS_ENDPOINT)

    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_obter_datas_lives_ocorridas_erro_servidor(
    client: FlaskClient, membro_token
):
    patch_target = (
        'acutis_api.application.use_cases.lives.'
        'listar.obter_datas_lives_ocorridas.'
        'ObterDatasLivesOcorridasUseCase.execute'
    )

    with patch(patch_target) as mock_execute:
        mock_execute.side_effect = Exception('Erro interno')

        response = client.get(
            OBTER_DATAS_LIVES_OCORRIDAS_ENDPOINT,
            headers={'Authorization': f'Bearer {membro_token}'},
        )

        assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
