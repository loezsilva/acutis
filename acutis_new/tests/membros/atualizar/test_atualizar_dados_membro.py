from http import HTTPStatus

from flask.testing import FlaskClient

ROTA_ATUALIZAR_DADOS_MEMBRO = '/api/membros/atualizar-dados-membro'


def test_atualizar_dados_membro_sucesso(
    client: FlaskClient, seed_registrar_membro, membro_token
):
    lead, membro, endereco = seed_registrar_membro()

    dados_atualizados = {
        'data_nascimento': '2002-06-26',
        'endereco': {
            'bairro': 'Centro',
            'cidade': 'São Paulo',
            'codigo_postal': '01001-000',
            'complemento': 'Apto 101',
            'estado': 'SP',
            'logradouro': 'Rua Exemplo',
            'numero': '123',
            'pais': 'Brasil',
            'tipo_logradouro': 'Rua',
        },
        'nome_social': 'Nome Atualizado',
    }

    response = client.put(
        ROTA_ATUALIZAR_DADOS_MEMBRO,
        json=dados_atualizados,
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json
    assert data['msg'] == 'Membro atualizado com sucesso.'


def test_atualizar_dados_membro_dados_invalidos(
    client: FlaskClient, membro_token
):
    dados = {
        'data_nascimento': 'data invalida',
        'endereco': {
            'codigo_postal': 'sem-numero',
            'estado': 'ZZ',
        },
        'nome_social': '',
    }

    response = client.put(
        ROTA_ATUALIZAR_DADOS_MEMBRO,
        json=dados,
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_atualizar_dados_membro_sem_token(client: FlaskClient):
    response = client.put(
        ROTA_ATUALIZAR_DADOS_MEMBRO,
        json={'nome_social': 'Nome Teste'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
