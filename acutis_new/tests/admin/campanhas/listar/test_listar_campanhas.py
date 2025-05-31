from datetime import datetime
from http import HTTPStatus
from unittest.mock import patch

from flask.testing import FlaskClient

from acutis_api.application.use_cases.campanha.listar.campanhas import (
    ListarCampanhasUseCase,
)

ROTA = '/api/admin/campanhas/listar-campanhas'


def test_listar_campanhas_filtro_doacao(
    client: FlaskClient, seed_campanha_doacao, membro_token
):
    response = client.get(
        f'{ROTA}?objetivo=doacao',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK

    data = response.json
    assert 'campanhas' in data
    assert 'pagina' in data
    assert 'total' in data
    assert 'paginas' in data
    assert 'por_pagina' in data

    assert len(data['campanhas']) == 1
    assert data['pagina'] == 1
    assert data['por_pagina'] == 10  # noqa
    assert data['total'] == 1
    assert data['paginas'] == 1

    campanha = data['campanhas'][0]
    assert campanha['campanha']['id'] == str(seed_campanha_doacao.id)
    assert campanha['campanha']['objetivo'] == 'doacao'


def test_listar_campanhas_filtro_cadastro(
    client: FlaskClient, seed_campanha_cadastro, membro_token
):
    response = client.get(
        f'{ROTA}?objetivo=cadastro',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK

    data = response.json
    assert 'campanhas' in data
    assert 'pagina' in data
    assert 'total' in data
    assert 'paginas' in data
    assert 'por_pagina' in data

    assert len(data['campanhas']) == 1
    assert data['pagina'] == 1
    assert data['por_pagina'] == 10  # noqa
    assert data['total'] == 1
    assert data['paginas'] == 1

    campanha = data['campanhas'][0]
    assert campanha['campanha']['id'] == str(seed_campanha_cadastro.id)
    assert campanha['campanha']['objetivo'] == 'cadastro'


def test_listar_campanhas_filtro_pre_cadastro(
    client: FlaskClient,
    seed_campanha_pre_cadastro_com_landing_page,
    membro_token,
):
    response = client.get(
        f'{ROTA}?objetivo=pre_cadastro',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK

    data = response.json
    assert 'campanhas' in data
    assert 'pagina' in data
    assert 'total' in data
    assert 'paginas' in data
    assert 'por_pagina' in data

    assert len(data['campanhas']) == 1
    assert data['pagina'] == 1
    assert data['por_pagina'] == 10  # noqa
    assert data['total'] == 1
    assert data['paginas'] == 1

    campanha = data['campanhas'][0]
    assert campanha['campanha']['id'] == str(
        seed_campanha_pre_cadastro_com_landing_page.id
    )
    assert campanha['campanha']['objetivo'] == 'pre_cadastro'


def test_listar_campanhas_filtro_data_bad_request(
    client: FlaskClient,
    seed_campanha_cadastro,
    seed_campanha_doacao,
    seed_campanha_membros_oficiais,
    membro_token,
):
    data_inicial = datetime.now()
    data_final = datetime.now()

    response = client.get(
        f'{ROTA}?data_inicial={data_inicial}&data_final={data_final}',  # noqa
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_CONTENT

    assert response.get_json()[0]['msg'] == (
        "Value error, A data deve estar no formato 'Y-m-d'"
    )
    assert response.get_json()[1]['msg'] == (
        "Value error, A data deve estar no formato 'Y-m-d'"
    )


def test_listar_campanhas_filtro_data_sucess(
    client: FlaskClient,
    seed_campanha_cadastro,
    seed_campanha_doacao,
    seed_campanha_membros_oficiais,
    membro_token,
):
    data_inicial = datetime.now().strftime('%Y-%m-%d')
    data_final = datetime.now().strftime('%Y-%m-%d')

    response = client.get(
        f'{ROTA}?data_inicial={data_inicial}&data_final={data_final}',  # noqa
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.get_json()['total'] == 3  # NOQA


@patch.object(ListarCampanhasUseCase, 'execute')
def test_listar_campanhas_erro_interno_servidor(
    mock_target, client: FlaskClient, membro_token
):
    mock_target.side_effect = Exception('Erro interno no servidor')

    response = client.get(
        f'{ROTA}?objetivo=doacao',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert response.json == [{'msg': 'Erro interno no servidor.'}]
