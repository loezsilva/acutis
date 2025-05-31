from http import HTTPStatus

from flask.testing import FlaskClient


def test_editar_programacao_live_avulsa_sucesso(
    client: FlaskClient, seed_registrar_live_avulsa, membro_token
):
    _, live_avulsa = seed_registrar_live_avulsa

    payload = {
        'tipo_programacao': 'avulsa',
        'data_hora_inicio': '2025-05-10T19:00:00',
        'dia_semana': None,
    }

    response = client.put(
        f'/api/admin/lives/editar-programacao-live/{live_avulsa.id}',
        json=payload,
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json
    assert data['msg'] == 'Programação da live atualizada com sucesso.'


def test_editar_programacao_live_recorrente_sucesso(
    client: FlaskClient, seed_registrar_live_recorrente, membro_token
):
    _, live_recorrente = seed_registrar_live_recorrente

    payload = {
        'tipo_programacao': 'recorrente',
        'hora_inicio': '19:00:00',
        'data_hora_inicio': None,
        'dia_semana': 'terça',
    }

    response = client.put(
        f'/api/admin/lives/editar-programacao-live/{live_recorrente.id}',
        json=payload,
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json
    assert data['msg'] == 'Programação da live atualizada com sucesso.'


def test_editar_programacao_live_nao_encontrada(
    client: FlaskClient, membro_token
):
    payload = {
        'tipo_programacao': 'avulsa',
        'data_hora_inicio': '2025-05-10T19:00:00',
        'dia_semana': None,
    }

    id_inexistente = '123e4567-e89b-12d3-a456-426614174000'

    response = client.put(
        f'/api/admin/lives/editar-programacao-live/{id_inexistente}',
        json=payload,
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    data = response.json
    assert data[0]['msg'] == 'Não foram encontradas lives programadas.'
