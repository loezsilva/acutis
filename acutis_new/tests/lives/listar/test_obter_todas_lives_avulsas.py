from http import HTTPStatus
from unittest.mock import patch

from flask.testing import FlaskClient

LISTAR_TODAS_LIVES_AVULSAS_ENDPOINT = (
    '/api/admin/lives/obter-todas-lives-avulsas'
)


def test_obter_todas_lives_avulsas_sucesso(client: FlaskClient, membro_token):
    response = client.get(
        LISTAR_TODAS_LIVES_AVULSAS_ENDPOINT,
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK

    data = response.get_json()

    assert isinstance(data, dict)
    assert 'agendamentos_avulsos' in data
    assert isinstance(data['agendamentos_avulsos'], list)

    if data['agendamentos_avulsos']:
        live = data['agendamentos_avulsos'][0]
        assert 'agendamento_rec_id' in live
        assert 'fk_campanha_id' in live
        assert 'rede_social' in live
        assert 'tag' in live
        assert 'fk_live_id' in live
        assert 'data_hora_inicio' in live


def test_obter_todas_lives_avulsas_nenhuma_encontrada(
    client: FlaskClient, membro_token
):
    response = client.get(
        LISTAR_TODAS_LIVES_AVULSAS_ENDPOINT + '?tag=inexistente123456',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK

    data = response.get_json()

    assert isinstance(data, dict)
    assert data['total'] == 0
    assert data['agendamentos_avulsos'] == []


def test_obter_todas_lives_avulsas_erro_interno(
    client: FlaskClient, membro_token
):
    patch_target = (
        'acutis_api.application.use_cases.lives.'
        'listar.obter_todas_lives_avulsas.'
        'ObterTodasLivesAvulsasUseCase.execute'
    )
    with patch(patch_target) as mock_execute:
        mock_execute.side_effect = Exception('Erro inesperado')

        response = client.get(
            LISTAR_TODAS_LIVES_AVULSAS_ENDPOINT,
            headers={'Authorization': f'Bearer {membro_token}'},
        )

        assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR


def test_obter_todas_lives_avulsas_filtragem_rede_social(
    client: FlaskClient, membro_token
):
    response = client.get(
        LISTAR_TODAS_LIVES_AVULSAS_ENDPOINT + '?rede_social=facebook',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK

    data = response.get_json()

    assert isinstance(data, dict)
    assert 'agendamentos_avulsos' in data
    assert isinstance(data['agendamentos_avulsos'], list)

    if data['agendamentos_avulsos']:
        live = data['agendamentos_avulsos'][0]
        assert live['rede_social'] == 'facebook'


def test_obter_todas_lives_avulsas_filtragem_data_hora_inicio(
    client: FlaskClient, membro_token
):
    url = (
        f'{LISTAR_TODAS_LIVES_AVULSAS_ENDPOINT}?'
        'data_hora_inicio=2025-05-10T21:00:00'
    )

    response = client.get(
        url,
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK

    data = response.get_json()

    assert isinstance(data, dict)
    assert 'agendamentos_avulsos' in data
    assert isinstance(data['agendamentos_avulsos'], list)

    if data['agendamentos_avulsos']:
        live = data['agendamentos_avulsos'][0]
        assert live['data_hora_inicio'] == '2025-05-10 21:00'


def test_obter_todas_lives_avulsas_sem_live_associada(
    client: FlaskClient, membro_token
):
    response = client.get(
        LISTAR_TODAS_LIVES_AVULSAS_ENDPOINT + '?tag=inexistente',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK

    data = response.get_json()

    assert isinstance(data, dict)
    assert data['total'] == 0
    assert data['agendamentos_avulsos'] == []
