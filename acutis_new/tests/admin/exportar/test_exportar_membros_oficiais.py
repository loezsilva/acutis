import random
from http import HTTPStatus
from io import BytesIO

import pandas as pd
import requests
from flask.testing import FlaskClient

rota = '/api/admin/exportar/membros-oficiais'
colunas = [
    'id',
    'nome',
    'email',
    'status',
    'telefone',
    'criado_em',
    'pais',
    'sexo',
    'numero_documento',
    'atualizado_em',
    'data_nascimento',
    'atualizado_por',
    'fk_cargo_oficial_id',
    'fk_superior_id',
]


def test_exportar_oficiais(
    client: FlaskClient, seed_membros_oficial, membro_token
):
    colunas_para_exportar = random.sample(
        colunas, random.randint(1, len(colunas))
    )

    colunas_params = ','.join(colunas_para_exportar)

    response = client.get(
        f'{rota}?colunas={colunas_params}',
        headers={'Authorization': f'Bearer {membro_token}'},
    )
    assert response.status_code == HTTPStatus.OK


def test_exportar_oficiais_filtro_id(
    client: FlaskClient, seed_membros_oficial, membro_token
):
    oficial = seed_membros_oficial[1]

    colunas_para_exportar = random.sample(
        colunas, random.randint(1, len(colunas))
    )

    colunas_params = ','.join(colunas_para_exportar)

    response = client.get(
        f'{rota}?colunas={colunas_params}&id={oficial.id}',
        headers={'Authorization': f'Bearer {membro_token}'},
    )
    assert response.status_code == HTTPStatus.OK

    arquivo_excel = requests.get(response.get_json()['url'])

    assert arquivo_excel.status_code == HTTPStatus.OK

    csv = pd.read_excel(BytesIO(arquivo_excel.content))

    # for i in colunas_para_exportar:
    #     if i == 'fk_superior_id':
    #         i = 'superior'  # noqa

    #     if i == 'fk_cargo_oficial_id':
    #         i = 'cargo'  # noqa
    #     assert i in csv.columns
    assert csv.shape[0] == 1


def test_exportar_oficiais_filtro_data(
    client: FlaskClient, seed_membros_oficial, membro_token
):
    data = '2025-01-08'

    colunas_para_exportar = random.sample(
        colunas, random.randint(1, len(colunas))
    )

    colunas_params = ','.join(colunas_para_exportar)

    response = client.get(
        f'{rota}?colunas={colunas_params}&data_inicio={data}&data_fim={data}',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK

    arquivo_excel = requests.get(response.get_json()['url'])

    assert arquivo_excel.status_code == HTTPStatus.OK

    csv = pd.read_excel(BytesIO(arquivo_excel.content))

    # for i in colunas_para_exportar:
    #     if i == 'fk_superior_id':
    #         i = 'superior'  # noqa

    #     if i == 'fk_cargo_oficial_id':
    #         i = 'cargo'  # noqa
    #     assert i in csv.columns

    assert csv.shape[0] == 2  # noqa


def test_exportar_oficiais_filter_not_found(client: FlaskClient, membro_token):
    lead = '1c1e26d5-63a0-4c4b-aec7-55eda93f21a1'

    colunas_para_exportar = random.sample(
        colunas, random.randint(1, len(colunas))
    )

    colunas_params = ','.join(colunas_para_exportar)

    response = client.get(
        f'{rota}?colunas={colunas_params}&id={lead}',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK

    assert response.get_json() == {
        'msg': 'Exportados 0 registros',
        'url': None,
    }
