from http import HTTPStatus

from faker import Faker
from flask.testing import FlaskClient

faker = Faker('pt-BR')


def test_registrar_cadastro_vocacional_brasileiro(
    client: FlaskClient, seed_pre_cadastro_vocacional_aprovado_brasil
):
    pre_cadastro_vocacional, _ = seed_pre_cadastro_vocacional_aprovado_brasil

    data_criar_registro = {
        'fk_usuario_vocacional_id': pre_cadastro_vocacional.id,
        'documento_identidade': '58497023005',
        'pais': 'brasil',
        'data_nascimento': '1980-01-12',
        'codigo_postal': '01001000',
        'logradouro': 'Rua das Flores',
        'numero': '444',
        'complemento': 'Apto 301',
        'bairro': 'Centro',
        'cidade': 'São Paulo',
        'estado': 'SP',
        'tipo_logradouro': 'Rua',
    }

    response_success = client.post(
        '/api/vocacional/registrar-cadastro-vocacional',
        json=data_criar_registro,
    )

    assert response_success.status_code == HTTPStatus.CREATED
    data = response_success.get_json()
    assert data == {'msg': 'Cadastro vocacional registrado com sucesso.'}


def test_registrar_cadastro_vocacional_brasileiro_conflito(
    client: FlaskClient, seed_cadastro_vocacional_aprovado
):
    pre_cadastro_vocacional, _ = seed_cadastro_vocacional_aprovado()

    data_criar_registro = {
        'fk_usuario_vocacional_id': pre_cadastro_vocacional.id,
        'documento_identidade': '58497023005',
        'pais': 'brasil',
        'data_nascimento': '1980-01-12',
        'codigo_postal': '01001000',
        'logradouro': 'Rua das Flores',
        'numero': '444',
        'complemento': 'Apto 301',
        'bairro': 'Centro',
        'cidade': 'São Paulo',
        'estado': 'SP',
        'tipo_logradouro': 'Rua',
    }

    response_conflict = client.post(
        '/api/vocacional/registrar-cadastro-vocacional',
        json=data_criar_registro,
    )

    assert response_conflict.status_code == HTTPStatus.CONFLICT
    data_conflict = response_conflict.get_json()
    assert data_conflict == [
        {'msg': 'Cadastro vocacional já registrado anteriormente.'}
    ]


def test_registrar_cadastro_usuario_nao_encontrado(
    client: FlaskClient,
):
    data_criar_registro = {
        'fk_usuario_vocacional_id': 'DF48557E-1DA0-4B53-986F-E4A7D82238D8',
        'documento_identidade': '58497023005',
        'pais': 'brasil',
        'data_nascimento': '1980-01-12',
        'codigo_postal': '01001000',
        'logradouro': 'Rua das Flores',
        'numero': '444',
        'complemento': 'Apto 301',
        'bairro': 'Centro',
        'cidade': 'São Paulo',
        'estado': 'SP',
        'tipo_logradouro': 'Rua',
    }

    response_conflict = client.post(
        '/api/vocacional/registrar-cadastro-vocacional',
        json=data_criar_registro,
    )

    assert response_conflict.status_code == HTTPStatus.NOT_FOUND
    data_conflict = response_conflict.get_json()
    assert data_conflict == [{'msg': 'Usuário vocacional não encontrado.'}]


def test_registrar_cadastro_vocacional_brasileiro_reprovado(
    client: FlaskClient, seed_pre_cadastro_vocacional_reprovado
):
    pre_cadastro_vocacional, _ = seed_pre_cadastro_vocacional_reprovado

    data_criar_registro = {
        'fk_usuario_vocacional_id': pre_cadastro_vocacional.id,
        'documento_identidade': '58497023005',
        'pais': 'brasil',
        'data_nascimento': '1980-01-12',
        'codigo_postal': '01001000',
        'logradouro': 'Rua das Flores',
        'numero': '444',
        'complemento': 'Apto 301',
        'bairro': 'Centro',
        'cidade': 'São Paulo',
        'estado': 'SP',
        'tipo_logradouro': 'Rua',
    }

    response_success = client.post(
        '/api/vocacional/registrar-cadastro-vocacional',
        json=data_criar_registro,
    )

    assert response_success.status_code == HTTPStatus.CONFLICT
    data = response_success.get_json()
    assert data == [
        {
            'msg': 'Não é possível prosseguir pois seu cadastrado \
                foi marcado como recusado anteriomente.'
        }
    ]


def test_registrar_cadastro_vocacional_brasileiro_nao_aprovado(
    client: FlaskClient, seed_pre_cadastro_vocacional_pendentes
):
    pre_cadastro_vocacional = seed_pre_cadastro_vocacional_pendentes[0][0]

    data_criar_registro = {
        'fk_usuario_vocacional_id': pre_cadastro_vocacional.id,
        'documento_identidade': '58497023005',
        'pais': 'brasil',
        'data_nascimento': '1980-01-12',
        'codigo_postal': '01001000',
        'logradouro': 'Rua das Flores',
        'numero': '444',
        'complemento': 'Apto 301',
        'bairro': 'Centro',
        'cidade': 'São Paulo',
        'estado': 'SP',
        'tipo_logradouro': 'Rua',
    }

    response_success = client.post(
        '/api/vocacional/registrar-cadastro-vocacional',
        json=data_criar_registro,
    )

    assert response_success.status_code == HTTPStatus.CONFLICT
    data = response_success.get_json()
    assert data == [
        {'msg': 'É necessário ter o pre_cadastro aprovado para continuar.'}
    ]


def test_registrar_cadastro_vocacional_brasileiro_desistencia(
    client: FlaskClient, seed_pre_cadastro_vocacional_desistencia
):
    pre_cadastro_vocacional, _ = seed_pre_cadastro_vocacional_desistencia()

    data_criar_registro = {
        'fk_usuario_vocacional_id': pre_cadastro_vocacional.id,
        'documento_identidade': '58497023005',
        'pais': 'brasil',
        'data_nascimento': '1980-01-12',
        'codigo_postal': '01001000',
        'logradouro': 'Rua das Flores',
        'numero': '444',
        'complemento': 'Apto 301',
        'bairro': 'Centro',
        'cidade': 'São Paulo',
        'estado': 'SP',
        'tipo_logradouro': 'Rua',
    }

    response_success = client.post(
        '/api/vocacional/registrar-cadastro-vocacional',
        json=data_criar_registro,
    )

    assert response_success.status_code == HTTPStatus.CONFLICT
    data = response_success.get_json()
    assert data == [
        {
            'msg': 'Não é possível prosseguir pois encontramos \
                um registro de desistência no seu processo vocacional.'
        }
    ]


def test_registrar_cadastro_vocacional_brasileiro_cpf_ja_cadastrado(
    client: FlaskClient,
    seed_pre_cadastro_vocacional_aprovado,
    seed_cadastro_vocacional_pendente,
):
    pre_cadastro_vocacional, _ = seed_pre_cadastro_vocacional_aprovado

    cadastro_vocacional = seed_cadastro_vocacional_pendente

    data_criar_registro = {
        'fk_usuario_vocacional_id': pre_cadastro_vocacional.id,
        'documento_identidade': cadastro_vocacional.documento_identidade,
        'pais': 'brasil',
        'data_nascimento': '1980-01-12',
        'codigo_postal': '01001000',
        'logradouro': 'Rua das Flores',
        'numero': '444',
        'complemento': 'Apto 301',
        'bairro': 'Centro',
        'cidade': 'São Paulo',
        'estado': 'SP',
        'tipo_logradouro': 'Rua',
    }

    response_conflict_cpf = client.post(
        '/api/vocacional/registrar-cadastro-vocacional',
        json=data_criar_registro,
    )

    assert response_conflict_cpf.status_code == HTTPStatus.CONFLICT
    data = response_conflict_cpf.get_json()
    assert data == [
        {'msg': 'Número do documento de identificação já cadastrado.'}
    ]


def test_registrar_cadastro_vocacional_estrangeiro_com_campos_de_endereco(
    client: FlaskClient, seed_pre_cadastro_vocacional_aprovado
):
    pre_cadastro_vocacional, _ = seed_pre_cadastro_vocacional_aprovado

    data_criar_registro = {
        'fk_usuario_vocacional_id': pre_cadastro_vocacional.id,
        'documento_identidade': '58497023424242005',
        'pais': 'uruguao',
        'data_nascimento': '1980-01-12',
        'logradouro': 'Rua das Flores',
        'numero': '444',
        'complemento': 'Apto 301',
        'bairro': 'Centro',
        'cidade': 'São Paulo',
        'estado': 'SP',
        'tipo_logradouro': 'Rua',
        'codigo_postal': '01001000',
    }

    response_success = client.post(
        '/api/vocacional/registrar-cadastro-vocacional',
        json=data_criar_registro,
    )

    assert response_success.status_code == HTTPStatus.CREATED
    data = response_success.get_json()
    assert data == {'msg': 'Cadastro vocacional registrado com sucesso.'}


def test_registrar_cadastro_vocacional_estrangeiro_campos_de_endereco_conflito(
    client: FlaskClient, seed_cadastro_vocacional_aprovado
):
    pre_cadastro_vocacional, _ = seed_cadastro_vocacional_aprovado()

    data_criar_registro = {
        'fk_usuario_vocacional_id': pre_cadastro_vocacional.id,
        'documento_identidade': '58497023424242005',
        'pais': 'uruguao',
        'data_nascimento': '1980-01-12',
        'logradouro': 'Rua das Flores',
        'numero': '444',
        'complemento': 'Apto 301',
        'bairro': 'Centro',
        'cidade': 'São Paulo',
        'estado': 'SP',
        'tipo_logradouro': 'Rua',
        'codigo_postal': '01001000',
    }

    response_conflict = client.post(
        '/api/vocacional/registrar-cadastro-vocacional',
        json=data_criar_registro,
    )

    assert response_conflict.status_code == HTTPStatus.CONFLICT
    data_conflict = response_conflict.get_json()
    assert data_conflict == [
        {'msg': 'Cadastro vocacional já registrado anteriormente.'}
    ]
