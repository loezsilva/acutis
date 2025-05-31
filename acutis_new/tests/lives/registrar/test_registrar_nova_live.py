from http import HTTPStatus
from unittest.mock import patch

import pytest
from faker import Faker
from flask.testing import FlaskClient

REGISTRAR_NOVA_LIVE_ENDPOINT = '/api/admin/lives/registrar-live'

faker = Faker(locale='pt-BR')


def test_registrar_live_avulsa_sucesso(
    client,
    seed_registrar_canal,
    membro_token,
):
    canal = seed_registrar_canal

    payload = {
        'tipo': 'avulsa',
        'canais_ids': [str(canal.id)],
        'data_hora_inicio': '2025-04-30T14:00:00',
    }

    response = client.post(
        REGISTRAR_NOVA_LIVE_ENDPOINT,
        json=payload,
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json['msg'] == 'Live registrada com sucesso.'


def test_registrar_live_recorrente_sucesso(
    client,
    seed_registrar_canal,
    membro_token,
):
    canal = seed_registrar_canal

    payload = {
        'tipo': 'recorrente',
        'canais_ids': [str(canal.id)],
        'programacoes': [
            {'dia_semana': 'segunda', 'hora_inicio': '18:00:00'},
            {'dia_semana': 'sexta', 'hora_inicio': '10:00:00'},
        ],
    }

    response = client.post(
        REGISTRAR_NOVA_LIVE_ENDPOINT,
        json=payload,
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json['msg'] == 'Live registrada com sucesso.'


@pytest.mark.parametrize(
    'campo_faltando', ['tag', 'fk_campanha_id', 'rede_social', 'criado_por']
)
def test_registrar_nova_live_campo_obrigatorio_faltando(
    client: FlaskClient,
    seed_nova_campanha,
    seed_registrar_membro,
    campo_faltando,
    membro_token,
):
    campanha = seed_nova_campanha()
    membro = seed_registrar_membro()[1]

    payload = {
        'tag': 'Live Teste',
        'fk_campanha_id': str(campanha.id),
        'rede_social': 'YouTube',
        'criado_por': str(membro.id),
    }

    del payload[campo_faltando]

    response = client.post(
        REGISTRAR_NOVA_LIVE_ENDPOINT,
        json=payload,
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_registrar_live_erro(client: FlaskClient, membro_token):
    patch_target = (
        'acutis_api.infrastructure.repositories.lives.'
        'LivesRepository.registrar_live_avulsa'
    )

    with patch(patch_target) as mock_registrar_live:
        mock_registrar_live.side_effect = Exception('Erro inesperado')

        payload = {
            'tipo': 'avulsa',
            'canais_ids': ['inexistente'],
            'data_hora_inicio': '2025-04-30T14:00:00',
        }

        response = client.post(
            REGISTRAR_NOVA_LIVE_ENDPOINT,
            json=payload,
            headers={'Authorization': f'Bearer {membro_token}'},
        )

        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
