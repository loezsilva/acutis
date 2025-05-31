from http import HTTPStatus
from unittest.mock import patch

from flask.testing import FlaskClient

LISTAR_LIVES_RECORRENTES_ENDPOINT = (
    '/api/admin/lives/obter-todas-lives-recorrentes'
)


def test_obter_todas_lives_recorrentes_sucesso(
    client: FlaskClient, seed_registrar_live_recorrente, membro_token
):
    response = client.get(
        LISTAR_LIVES_RECORRENTES_ENDPOINT,
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK

    data = response.get_json()

    assert isinstance(data, dict)
    assert 'agendamentos_recorrentes' in data
    assert isinstance(data['agendamentos_recorrentes'], list)

    if data['agendamentos_recorrentes']:
        live = data['agendamentos_recorrentes'][0]
        assert 'agendamento_rec_id' in live
        assert 'campanha_id' in live
        assert 'dia_semana' in live
        assert 'rede_social' in live
        assert 'tag' in live
        assert 'live_id' in live
        assert 'hora_inicio' in live


def test_obter_todas_lives_recorrentes_nenhuma_encontrada(
    client: FlaskClient, membro_token
):
    response = client.get(
        LISTAR_LIVES_RECORRENTES_ENDPOINT + '?tag=inexistente123456',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK

    data = response.get_json()

    assert isinstance(data, dict)
    assert data['total'] == 0
    assert data['agendamentos_recorrentes'] == []


def test_obter_todas_lives_recorrentes_erro_interno(
    client: FlaskClient, membro_token
):
    patch_target = (
        'acutis_api.application.use_cases.lives.'
        'listar.obter_todas_lives_recorrentes.'
        'ObterTodasLivesRecorrentesUseCase.execute'
    )
    with patch(patch_target) as mock_execute:
        mock_execute.side_effect = Exception('Erro inesperado')

        response = client.get(
            LISTAR_LIVES_RECORRENTES_ENDPOINT,
            headers={'Authorization': f'Bearer {membro_token}'},
        )

        assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
