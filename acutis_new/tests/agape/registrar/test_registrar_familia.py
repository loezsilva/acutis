import json
from http import HTTPStatus
from io import BytesIO

from faker import Faker
from flask.testing import FlaskClient

REGISTRAR_FAMILIA_ENDPOINT = '/api/agape/registrar-familia'

faker = Faker(locale='pt-BR')


def pegar_dados():
    endereco = json.dumps({
        'cep': '58000000',
        'rua': 'Av. almirante carvalho',
        'bairro': 'bairro teste',
        'cidade': 'cidade teste',
        'estado': 'ce',
        'numero': '1250',
        'complemento': 'complemento teste',
    })

    membros = [
        json.dumps({
            'responsavel': True,
            'nome': 'nome teste',
            'email': faker.email(domain='headers.com.br'),
            'telefone': '986781358',
            'nome_social': 'nome social teste',
            'cpf': '30607778024',
            'data_nascimento': '1998-01-21',
            'funcao_familiar': 'pai',
            'escolaridade': 'ensino médio completo',
            'ocupacao': 'de teste',
            'renda': None,
            'beneficiario_assistencial': False,
        })
    ]

    dados = {
        'endereco': endereco,
        'membros': membros,
        'observacao': 'teste',
    }

    arquivos = {
        'comprovante_residencia': (BytesIO(b'foto'), 'foto_teste.png'),
        'fotos_familia': [(BytesIO(b'foto'), 'foto_teste.png')],
    }

    return dados, arquivos


def test_registrar_familia_sucesso(client: FlaskClient, membro_token):
    dados, arquivos = pegar_dados()

    response = client.post(
        REGISTRAR_FAMILIA_ENDPOINT,
        headers={'Authorization': f'Bearer {membro_token}'},
        data={**dados, **arquivos},
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json['msg'].lower() == 'família cadastrada com sucesso.'


def test_erro_registrar_familia_cep_invalido(
    client: FlaskClient, membro_token
):
    dados, _ = pegar_dados()
    dados['endereco'] = json.dumps({
        'cep': '58000-000',
        'rua': 'Av. almirante carvalho',
        'bairro': 'bairro teste',
        'cidade': 'cidade teste',
        'estado': 'ce',
        'numero': '1250',
        'complemento': 'complemento teste',
    })

    response = client.post(
        REGISTRAR_FAMILIA_ENDPOINT,
        headers={'Authorization': f'Bearer {membro_token}'},
        data=dados,
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert 'cep' == response.json[0]['type']
