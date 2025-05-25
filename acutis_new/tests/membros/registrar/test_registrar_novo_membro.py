import json
from http import HTTPStatus
from io import BytesIO

from faker import Faker
from flask.testing import FlaskClient

from acutis_api.domain.entities.lead import Lead
from acutis_api.domain.entities.lead_campanha import LeadCampanha
from acutis_api.infrastructure.extensions import database

REGISTRAR_NOVO_MEMBRO_ENDPOINT = '/api/membros/registrar-novo-membro'

faker = Faker(locale='pt-BR')


def test_registrar_novo_membro_sucesso(client: FlaskClient):
    nome = ' '.join(faker.words(2))

    endereco = json.dumps({
        'codigo_postal': '60806-59',
        'tipo_logradouro': 'rua',
        'logradouro': 'Av. almirante carvalho 1',
        'numero': '1250',
        'complemento': 'complemento teste 1',
        'bairro': 'bairro teste 1',
        'cidade': 'cidade teste 1',
        'estado': 'ce',
        'pais': 'brasil',
    })
    membro = json.dumps({
        'nome': nome,
        'nome_social': nome,
        'email': faker.email(domain='headers.com.br'),
        'numero_documento': faker.cpf(),
        'telefone': faker.cellphone_number(),
        'data_nascimento': '1998-01-21',
        'sexo': 'masculino',
        'origem_cadastro': 'acutis',
    })

    foto = (BytesIO(b'foto'), 'foto_teste1.png')

    response = client.post(
        REGISTRAR_NOVO_MEMBRO_ENDPOINT,
        data={'membro': membro, 'endereco': endereco, 'foto': foto},
    )

    assert response.status_code == HTTPStatus.CREATED
    assert 'id' in response.json
    assert response.json['nome'] == nome.title()

    lead = database.session.get(Lead, response.json['id'])
    assert lead is not None
    assert not lead.status
    assert lead.membro is not None
    assert lead.membro.endereco is not None


def test_registrar_novo_membro_pelo_google_sucesso(client: FlaskClient):
    with client.session_transaction() as sess:
        sess['google_auth'] = True

    nome = ' '.join(faker.words(2))

    endereco = json.dumps({
        'codigo_postal': '60806-59',
        'tipo_logradouro': 'rua',
        'logradouro': 'Av. almirante carvalho 1',
        'numero': '1250',
        'complemento': 'complemento teste 1',
        'bairro': 'bairro teste 1',
        'cidade': 'cidade teste 1',
        'estado': 'ce',
        'pais': 'brasil',
    })
    membro = json.dumps({
        'nome': nome,
        'nome_social': nome,
        'email': faker.email(domain='headers.com.br'),
        'numero_documento': faker.cpf(),
        'telefone': faker.cellphone_number(),
        'data_nascimento': '1998-01-21',
        'sexo': 'masculino',
        'senha': '#Teste@12345',
        'origem_cadastro': 'acutis',
    })

    foto = (BytesIO(b'foto2'), 'foto_teste2.png')

    response = client.post(
        REGISTRAR_NOVO_MEMBRO_ENDPOINT,
        data={'membro': membro, 'endereco': endereco, 'foto': foto},
    )

    assert response.status_code == HTTPStatus.CREATED
    assert 'id' in response.json
    assert response.json['nome'] == nome.title()

    lead = database.session.get(Lead, response.json['id'])
    assert lead is not None
    assert lead.status
    assert lead.membro is not None
    assert lead.membro.endereco is not None


def test_registrar_novo_membro_com_campanha_origem_sucesso(
    client: FlaskClient, seed_nova_campanha
):
    campanha = seed_nova_campanha()
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
        'nome_social': 'nome social teste',
        'email': 'emailtest@gmail.com',
        'numero_documento': '306.077.780-24',
        'telefone': '(96) 98678-1358',
        'data_nascimento': '1998-01-21',
        'sexo': 'masculino',
        'origem_cadastro': 'acutis',
    })
    foto = (BytesIO(b'foto teste'), 'foto_teste.png')

    response = client.post(
        REGISTRAR_NOVO_MEMBRO_ENDPOINT,
        data={
            'membro': membro,
            'endereco': endereco,
            'foto': foto,
            'campanha_id': campanha.id,
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert 'id' in response.json
    assert response.json['nome'] == 'Nome Teste'

    lead = database.session.get(Lead, response.json['id'])
    assert lead is not None
    assert lead.membro is not None
    assert lead.membro.endereco is not None

    lead_campanha = database.session.query(LeadCampanha).filter_by(
        fk_lead_id=lead.id, fk_campanha_id=campanha.id
    )
    assert lead_campanha is not None


def test_erro_email_ja_cadastrado(client: FlaskClient, seed_registrar_membro):
    lead = seed_registrar_membro()[0]

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
        'nome_social': 'nome social teste',
        'email': lead.email,
        'numero_documento': '306.077.780-24',
        'telefone': '(96) 98678-1358',
        'data_nascimento': '1998-01-21',
        'sexo': 'masculino',
        'senha': '#Teste@123',
        'origem_cadastro': 'acutis',
    })

    foto = (BytesIO(b'foto teste'), 'foto_teste.png')

    response = client.post(
        REGISTRAR_NOVO_MEMBRO_ENDPOINT,
        data={'membro': membro, 'endereco': endereco, 'foto': foto},
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json == [{'msg': 'Email já cadastrado.'}]


def test_erro_documento_ja_cadastrado(
    client: FlaskClient, seed_registrar_membro
):
    membro = seed_registrar_membro()[1]

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
        'nome_social': 'nome social teste',
        'email': 'emailtest@gmail.com',
        'numero_documento': membro.numero_documento,
        'telefone': '(96) 98678-1358',
        'data_nascimento': '1998-01-21',
        'sexo': 'masculino',
        'senha': '#Teste@123',
        'origem_cadastro': 'acutis',
    })

    foto = (BytesIO(b'foto teste'), 'foto_teste.png')

    response = client.post(
        REGISTRAR_NOVO_MEMBRO_ENDPOINT,
        data={'membro': membro, 'endereco': endereco, 'foto': foto},
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json == [{'msg': 'Número documento já cadastrado.'}]


def test_registrar_novo_membro_erro_campanha_inativa(
    client: FlaskClient, seed_nova_campanha
):
    campanha = seed_nova_campanha(ativa=False)
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
        'nome_social': 'nome social teste',
        'email': 'emailtest@gmail.com',
        'numero_documento': '306.077.780-24',
        'telefone': '(96) 98678-1358',
        'data_nascimento': '1998-01-21',
        'sexo': 'masculino',
        'senha': '#Teste@123',
        'origem_cadastro': 'acutis',
    })

    response = client.post(
        REGISTRAR_NOVO_MEMBRO_ENDPOINT,
        data={
            'membro': membro,
            'endereco': endereco,
            'campanha_id': campanha.id,
        },
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json == [
        {'msg': 'Ops, a campanha está inativa e não pode receber cadastros.'}
    ]


def test_registrar_novo_membro_erro_campanha_nao_encontrada(
    client: FlaskClient,
):
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
        'nome_social': 'nome social teste',
        'email': 'emailtest@gmail.com',
        'numero_documento': '306.077.780-24',
        'telefone': '(96) 98678-1358',
        'data_nascimento': '1998-01-21',
        'sexo': 'masculino',
        'senha': '#Teste@123',
        'origem_cadastro': 'acutis',
    })

    response = client.post(
        REGISTRAR_NOVO_MEMBRO_ENDPOINT,
        data={
            'membro': membro,
            'endereco': endereco,
            'campanha_id': 'c1ea2406-62de-48e7-baa8-8dd46eb532f0',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json == [{'msg': 'Ops, Campanha não encontrada.'}]
