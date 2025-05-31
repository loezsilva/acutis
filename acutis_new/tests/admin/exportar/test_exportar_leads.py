import random
from http import HTTPStatus

import requests
from flask.testing import FlaskClient

rota = '/api/admin/exportar/leads'
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
]


def test_exportar_leads(
    client: FlaskClient, seed_leads_por_origem, membro_token
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
    # assert csv.shape[0] == 13  # noqa


def test_exportar_leads_filter_not_found(client: FlaskClient, membro_token):
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


def test_exportar_leads_filter_id(
    client: FlaskClient, seed_leads_por_origem, membro_token
):
    lead = seed_leads_por_origem[5]

    colunas_para_exportar = random.sample(
        colunas, random.randint(1, len(colunas))
    )

    colunas_params = ','.join(colunas_para_exportar)

    response = client.get(
        f'{rota}?colunas={colunas_params}&id={lead.id}',
        headers={'Authorization': f'Bearer {membro_token}'},
    )
    assert response.status_code == HTTPStatus.OK

    arquivo_excel = requests.get(response.get_json()['url'])

    assert arquivo_excel.status_code == HTTPStatus.OK

    # csv = pd.read_excel(BytesIO(arquivo_excel.content))

    # for i in colunas_para_exportar:
    #     assert i in csv.columns
    # assert csv.shape[0] == 1  # noqa


def test_exportar_leads_filter_email(
    client: FlaskClient, seed_leads_por_origem, membro_token
):
    lead = seed_leads_por_origem[1]

    colunas_para_exportar = random.sample(
        colunas, random.randint(1, len(colunas))
    )

    colunas_params = ','.join(colunas_para_exportar)

    response = client.get(
        f'{rota}?colunas={colunas_params}&email={lead.email}',
        headers={'Authorization': f'Bearer {membro_token}'},
    )
    assert response.status_code == HTTPStatus.OK

    arquivo_excel = requests.get(response.get_json()['url'])

    assert arquivo_excel.status_code == HTTPStatus.OK

    # csv = pd.read_excel(BytesIO(arquivo_excel.content))

    # for i in colunas_para_exportar:
    #     assert i in csv.columns
    # assert csv.shape[0] == 1  # noqa


def test_exportar_leads_filter_data(
    client: FlaskClient, seed_registra_13_leads, membro_token
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

    # for i in colunas_para_exportar:
    #     assert i in csv.columns
    # assert csv.shape[0] == 2  # noqa


def test_exportar_leads_filter_nome(
    client: FlaskClient, seed_leads_por_origem, membro_token
):
    lead = seed_leads_por_origem[1]

    colunas_para_exportar = random.sample(
        colunas, random.randint(1, len(colunas))
    )

    colunas_params = ','.join(colunas_para_exportar)

    response = client.get(
        f'{rota}?colunas={colunas_params}&nome={lead.nome}',
        headers={'Authorization': f'Bearer {membro_token}'},
    )
    assert response.status_code == HTTPStatus.OK

    arquivo_excel = requests.get(response.get_json()['url'])

    assert arquivo_excel.status_code == HTTPStatus.OK

    # csv = pd.read_excel(BytesIO(arquivo_excel.content))

    # for i in colunas_para_exportar:
    #     assert i in csv.columns
    # assert csv.shape[0] == 1  # noqa


def test_exportar_leads_filter_pais(
    client: FlaskClient, seed_leads_por_origem, membro_token
):
    colunas_para_exportar = random.sample(
        colunas, random.randint(1, len(colunas))
    )

    colunas_params = ','.join(colunas_para_exportar)

    response = client.get(
        f'{rota}?colunas={colunas_params}&pais=pais_especifico',
        headers={'Authorization': f'Bearer {membro_token}'},
    )
    assert response.status_code == HTTPStatus.OK

    arquivo_excel = requests.get(response.get_json()['url'])

    assert arquivo_excel.status_code == HTTPStatus.OK

    # csv = pd.read_excel(BytesIO(arquivo_excel.content))

    # for i in colunas_para_exportar:
    #     assert i in csv.columns
    # assert csv.shape[0] == 4  # noqa


def test_exportar_leads_filter_campanha(
    client: FlaskClient, seed_15_leads_campanhas, membro_token
):
    campanha = seed_15_leads_campanhas[-1]

    colunas_para_exportar = random.sample(
        colunas, random.randint(1, len(colunas))
    )

    colunas_params = ','.join(colunas_para_exportar)

    response = client.get(
        f'{rota}?colunas={colunas_params}&campanha={campanha["campanha_id"]}',
        headers={'Authorization': f'Bearer {membro_token}'},
    )
    assert response.status_code == HTTPStatus.OK

    arquivo_excel = requests.get(response.get_json()['url'])

    assert arquivo_excel.status_code == HTTPStatus.OK

    # csv = pd.read_excel(BytesIO(arquivo_excel.content))

    # for i in colunas_para_exportar:
    #     assert i in csv.columns
    # assert csv.shape[0] == 5  # noqa


def test_exportar_leads_filter_origem_cadastro(
    client: FlaskClient, seed_leads_por_origem, membro_token
):
    colunas_para_exportar = random.sample(
        colunas, random.randint(1, len(colunas))
    )

    colunas_params = ','.join(colunas_para_exportar)

    response = client.get(
        f'{rota}?colunas={colunas_params}&origem_cadastro=google',
        headers={'Authorization': f'Bearer {membro_token}'},
    )
    assert response.status_code == HTTPStatus.OK

    arquivo_excel = requests.get(response.get_json()['url'])

    assert arquivo_excel.status_code == HTTPStatus.OK

    # csv = pd.read_excel(BytesIO(arquivo_excel.content))

    # for i in colunas_para_exportar:
    #     assert i in csv.columns
    # assert csv.shape[0] == 4  # noqa
