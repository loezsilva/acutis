from http import HTTPStatus
from unittest.mock import patch

from flask.testing import FlaskClient

from acutis_api.application.use_cases.admin.membros import (
    BuscarDoacoesECampanhasDoMembroUseCase,
)

DOACOES_E_CAMPANHAS_MEMBRO_ENDPOINT = (
    '/api/admin/membros/buscar-doacoes-e-campanhas-membro'
)


def test_buscar_dados_doacoes_e_campanhas_do_membro(
    client: FlaskClient, seed_membro_com_doacao_e_campanha, membro_token
):
    qtd_doacoes = 1
    qtd_campanhas = 1
    qtd_total_doacoes = 10.0

    _, membro, _, _ = seed_membro_com_doacao_e_campanha

    membro_id = membro.id

    response = client.get(
        f'{DOACOES_E_CAMPANHAS_MEMBRO_ENDPOINT}/{membro_id}',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json['data_ultima_doacao'] is not None
    assert response.json['num_doacoes'] == qtd_doacoes
    assert response.json['num_registros_em_campanhas'] == qtd_campanhas
    assert response.json['quantia_total_doada'] == qtd_total_doacoes


def test_doacoes_e_campanhas_membro_sem_autenticacao(
    client: FlaskClient, seed_membro_com_doacao_e_campanha
):
    _, membro, _, _ = seed_membro_com_doacao_e_campanha

    membro_id = membro.id

    response = client.get(
        f'{DOACOES_E_CAMPANHAS_MEMBRO_ENDPOINT}/{membro_id}',
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_membro_sem_doacoes_ou_campanhas(
    client: FlaskClient, seed_registrar_membro, membro_token
):
    _, membro, _ = seed_registrar_membro()

    membro_id = membro.id

    response = client.get(
        f'{DOACOES_E_CAMPANHAS_MEMBRO_ENDPOINT}/{membro_id}',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json

    assert data['num_doacoes'] == 0
    assert data['quantia_total_doada'] == 0
    assert data['num_registros_em_campanhas'] == 0
    assert data['data_ultima_doacao'] is None


def test_buscar_doacoes_e_campanhas_membro_inexistente_ok(
    client: FlaskClient, membro_token
):
    membro_id = '123e4567-e89b-12d3-a456-426614174000'

    response = client.get(
        f'{DOACOES_E_CAMPANHAS_MEMBRO_ENDPOINT}/{membro_id}',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json
    assert data['num_doacoes'] == 0
    assert data['quantia_total_doada'] == 0
    assert data['num_registros_em_campanhas'] == 0
    assert data['data_ultima_doacao'] is None


@patch.object(BuscarDoacoesECampanhasDoMembroUseCase, 'execute')
def test_buscar_doacoes_e_campanhas_membro_erro_interno_servidor(
    mock_target,
    client: FlaskClient,
    membro_token,
    seed_membro_com_doacao_e_campanha,
):
    mock_target.side_effect = Exception('Erro interno no servidor')

    _, membro, _, _ = seed_membro_com_doacao_e_campanha

    membro_id = membro.id

    response = client.get(
        f'{DOACOES_E_CAMPANHAS_MEMBRO_ENDPOINT}/{membro_id}',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert response.json == [{'msg': 'Erro interno no servidor.'}]
