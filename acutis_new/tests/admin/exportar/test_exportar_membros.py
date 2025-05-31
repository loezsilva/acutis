import random
from http import HTTPStatus

import requests
from flask.testing import FlaskClient

rota = '/api/admin/exportar/membros'
colunas = [
    'id',
    'nome',
    'email',
    'status',
    'telefone',
    'origem_cadastro',
    'criado_em',
    'ultimo_acesso',
    'pais',
    'sexo',
    'fk_lead_id',
    'numero_documento',
]


def test_exportar_membros(
    client: FlaskClient, seed_registra_15_membros_idade, membro_token
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

    arquivo_excel = requests.get(response.get_json()['url'])

    assert arquivo_excel.status_code == HTTPStatus.OK

    # csv = pd.read_excel(BytesIO(arquivo_excel.content))

    # for i in colunas_para_exportar:
    #     assert i in csv.columns
    # assert csv.shape[0] == 16  # noqa


def test_exportar_membros_filter_not_found(client: FlaskClient, membro_token):
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


def test_exportar_membro_filter_id(
    client: FlaskClient, seed_registra_15_membros_idade, membro_token
):
    membro = seed_registra_15_membros_idade[5]

    colunas_para_exportar = random.sample(
        colunas, random.randint(1, len(colunas))
    )

    colunas_params = ','.join(colunas_para_exportar)

    response = client.get(
        f'{rota}?colunas={colunas_params}&id={membro.id}',
        headers={'Authorization': f'Bearer {membro_token}'},
    )
    assert response.status_code == HTTPStatus.OK

    arquivo_excel = requests.get(response.get_json()['url'])

    assert arquivo_excel.status_code == HTTPStatus.OK

    # csv = pd.read_excel(BytesIO(arquivo_excel.content))

    # for i in colunas_para_exportar:
    #     assert i in csv.columns
    # assert csv.shape[0] == 1  # noqa


def test_exportar_membro_filter_numero_documento(
    client: FlaskClient, seed_registra_15_membros_idade, membro_token
):
    membro = seed_registra_15_membros_idade[5]

    colunas_para_exportar = random.sample(
        colunas, random.randint(1, len(colunas))
    )

    colunas_params = ','.join(colunas_para_exportar)

    response = client.get(
        f'{rota}?colunas={colunas_params}&numero_documento={
            membro.numero_documento
        }',
        headers={'Authorization': f'Bearer {membro_token}'},
    )
    assert response.status_code == HTTPStatus.OK

    arquivo_excel = requests.get(response.get_json()['url'])

    assert arquivo_excel.status_code == HTTPStatus.OK

    # csv = pd.read_excel(BytesIO(arquivo_excel.content))

    # for i in colunas_para_exportar:
    #     assert i in csv.columns
    # assert csv.shape[0] == 1  # noqa


def test_exportar_membro_filter_campanha(
    client: FlaskClient, seed_registra_5_membros_campanha, membro_token
):
    campanha = seed_registra_5_membros_campanha[1]

    colunas_para_exportar = random.sample(
        colunas, random.randint(1, len(colunas))
    )

    colunas_params = ','.join(colunas_para_exportar)

    response = client.get(
        f'{rota}?colunas={colunas_params}&campanha={campanha.id}',
        headers={'Authorization': f'Bearer {membro_token}'},
    )
    assert response.status_code == HTTPStatus.OK

    arquivo_excel = requests.get(response.get_json()['url'])

    assert arquivo_excel.status_code == HTTPStatus.OK

    # csv = pd.read_excel(BytesIO(arquivo_excel.content))

    # for i in colunas_para_exportar:
    #     assert i in csv.columns
    # assert csv.shape[0] == 5  # noqa


def test_exportar_membros_filter_data(
    client: FlaskClient, seed_registra_10_membros, membro_token
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

    # csv = pd.read_excel(BytesIO(arquivo_excel.content))

    # # for i in colunas_para_exportar:
    # #     assert i in csv.columns
    # # assert csv.shape[0] == 2  # noqa
