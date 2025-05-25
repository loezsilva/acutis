import json
from http import HTTPStatus

from flask.testing import FlaskClient

REGISTRAR_NOVO_MEMBRO_ENDPOINT = '/api/membros/registrar-novo-membro'


def test_erro_nome_com_caracteres_invalidos(client: FlaskClient):
    endereco = json.dumps({
        'codigo_postal': '60806-59',
        'tipo_logradouro': 'rua',
        'logradouro': 'Av. almirante carvalho',
        'numero': '1250',
        'complemento': 'complemento teste',
        'bairro': 'bairro teste',
        'cidade': 'cidade teste',
        'estado': 'ce',
        'pais': 'brasil',
    })
    membro = json.dumps({
        'nome': 'Yan P1st0l3ir0',
        'nome_social': 'nome social teste',
        'email': 'emailtest@gmail.com',
        'numero_documento': '56983248756',
        'telefone': '(96) 98678-1358',
        'data_nascimento': '1998-01-21',
        'sexo': 'masculino',
        'senha': '#Teste@123',
        'origem_cadastro': 'acutis',
    })

    response = client.post(
        REGISTRAR_NOVO_MEMBRO_ENDPOINT,
        data={'membro': membro, 'endereco': endereco},
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json == [
        {
            'input': 'Yan P1st0l3ir0',
            'loc': ['membro', 'nome'],
            'msg': 'O nome Yan P1st0l3ir0 possui caracteres inválidos.',
            'type': 'value_error',
        }
    ]


def test_erro_nome_com_mais_de_100_caracteres(client: FlaskClient):
    endereco = json.dumps({
        'codigo_postal': '60806-59',
        'tipo_logradouro': 'rua',
        'logradouro': 'Av. almirante carvalho',
        'numero': '1250',
        'complemento': 'complemento teste',
        'bairro': 'bairro teste',
        'cidade': 'cidade teste',
        'estado': 'ce',
        'pais': 'brasil',
    })
    membro = json.dumps({
        'nome': 'MaximilianoSebastianoFilipeRodriguezAntonioFernandezGuillermoAlexandreTheodoroCristobalVasquezDominguezHernandez',  # noqa
        'nome_social': 'nome social teste',
        'email': 'emailtest@gmail.com',
        'numero_documento': '56983248756',
        'telefone': '(96) 98678-1358',
        'data_nascimento': '1998-01-21',
        'sexo': 'masculino',
        'senha': '#Teste@123',
        'origem_cadastro': 'acutis',
    })

    response = client.post(
        REGISTRAR_NOVO_MEMBRO_ENDPOINT,
        data={'membro': membro, 'endereco': endereco},
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json[0]['msg'] == (
        'O nome deve conter entre 3 e 100 caracteres.'
    )


def test_erro_nome_social_com_caracteres_invalidos(client: FlaskClient):
    endereco = json.dumps({
        'codigo_postal': '60806-59',
        'tipo_logradouro': 'rua',
        'logradouro': 'Av. almirante carvalho',
        'numero': '1250',
        'complemento': 'complemento teste',
        'bairro': 'bairro teste',
        'cidade': 'cidade teste',
        'estado': 'ce',
        'pais': 'brasil',
    })
    membro = json.dumps({
        'nome': 'nome teste',
        'nome_social': 'Joao Z3z1m',
        'email': 'emailtest@gmail.com',
        'numero_documento': '56983248756',
        'telefone': '(96) 98678-1358',
        'data_nascimento': '1998-01-21',
        'sexo': 'masculino',
        'senha': '#Teste@123',
        'origem_cadastro': 'acutis',
    })

    response = client.post(
        REGISTRAR_NOVO_MEMBRO_ENDPOINT,
        data={'membro': membro, 'endereco': endereco},
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json == [
        {
            'input': 'Joao Z3z1m',
            'loc': ['membro', 'nome_social'],
            'msg': 'O nome social Joao Z3z1m possui caracteres inválidos.',
            'type': 'value_error',
        }
    ]


def test_erro_numero_documento_com_menos_11_caracteres(client: FlaskClient):
    endereco = json.dumps({
        'codigo_postal': '60806-59',
        'tipo_logradouro': 'rua',
        'logradouro': 'Av. almirante carvalho',
        'numero': '1250',
        'complemento': 'complemento teste',
        'bairro': 'bairro teste',
        'cidade': 'cidade teste',
        'estado': 'ce',
        'pais': 'brasil',
    })
    membro = json.dumps({
        'nome': 'nome teste',
        'nome_social': 'teste nome social',
        'email': 'emailtest@gmail.com',
        'numero_documento': '56983248',
        'telefone': '(96) 98678-1358',
        'data_nascimento': '1998-01-21',
        'sexo': 'masculino',
        'senha': '#Teste@123',
        'origem_cadastro': 'acutis',
    })

    response = client.post(
        REGISTRAR_NOVO_MEMBRO_ENDPOINT,
        data={'membro': membro, 'endereco': endereco},
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json == [
        {
            'input': '56983248',
            'loc': ['membro', 'numero_documento'],
            'msg': 'O documento deve conter entre 11 e 50 caracteres.',
            'type': 'value_error',
        }
    ]


def test_erro_estado_com_mais_de_2_caracteres(client: FlaskClient):
    endereco = json.dumps({
        'codigo_postal': '60806-59',
        'tipo_logradouro': 'rua',
        'logradouro': 'Av. almirante carvalho',
        'numero': '1250',
        'complemento': 'complemento teste',
        'bairro': 'bairro teste',
        'cidade': 'cidade teste',
        'estado': 'Ceara',
        'pais': 'brasil',
    })
    membro = json.dumps({
        'nome': 'nome teste',
        'nome_social': 'teste nome social',
        'email': 'emailtest@gmail.com',
        'numero_documento': '56983248756',
        'telefone': '(96) 98678-1358',
        'data_nascimento': '1998-01-21',
        'sexo': 'masculino',
        'senha': '#Teste@123',
        'origem_cadastro': 'acutis',
    })

    response = client.post(
        REGISTRAR_NOVO_MEMBRO_ENDPOINT,
        data={'membro': membro, 'endereco': endereco},
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json == [
        {
            'input': 'Ceara',
            'loc': ['endereco', 'estado'],
            'msg': 'O campo "Estado" deve conter exatamente 2 caracteres.',
            'type': 'value_error',
        }
    ]


def test_erro_membro_json_invalido(client: FlaskClient):
    endereco = json.dumps({
        'codigo_postal': '60806-59',
        'tipo_logradouro': 'rua',
        'logradouro': 'Av. almirante carvalho',
        'numero': '1250',
        'complemento': 'complemento teste',
        'bairro': 'bairro teste',
        'cidade': 'cidade teste',
        'estado': 'Ceara',
        'pais': 'brasil',
    })
    membro = {
        'nome': 'nome teste',
        'nome_social': 'teste nome social',
        'email': 'emailtest@gmail.com',
        'numero_documento': '56983248756',
        'telefone': '(96) 98678-1358',
        'data_nascimento': '1998-01-21',
        'sexo': 'masculino',
        'senha': '#Teste@123',
        'origem_cadastro': 'acutis',
    }

    response = client.post(
        REGISTRAR_NOVO_MEMBRO_ENDPOINT,
        data={'membro': membro, 'endereco': endereco},
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert (
        response.json[0]['msg'] == 'O campo "membro" deve ser um JSON válido.'
    )


def test_erro_endereco_json_invalido(client: FlaskClient):
    endereco = {
        'codigo_postal': '60806-59',
        'tipo_logradouro': 'rua',
        'logradouro': 'Av. almirante carvalho',
        'numero': '1250',
        'complemento': 'complemento teste',
        'bairro': 'bairro teste',
        'cidade': 'cidade teste',
        'estado': 'Ceara',
        'pais': 'brasil',
    }
    membro = json.dumps({
        'nome': 'nome teste',
        'nome_social': 'teste nome social',
        'email': 'emailtest@gmail.com',
        'numero_documento': '56983248756',
        'telefone': '(96) 98678-1358',
        'data_nascimento': '1998-01-21',
        'sexo': 'masculino',
        'senha': '#Teste@123',
        'origem_cadastro': 'acutis',
    })

    response = client.post(
        REGISTRAR_NOVO_MEMBRO_ENDPOINT,
        data={'membro': membro, 'endereco': endereco},
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert (
        response.json[0]['msg']
        == 'O campo "endereco" deve ser um JSON válido.'
    )
