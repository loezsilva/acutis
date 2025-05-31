import json
from http import HTTPStatus
from io import BytesIO
from unittest.mock import patch

from flask.testing import FlaskClient

from acutis_api.domain.entities.campanha import Campanha
from acutis_api.infrastructure.extensions import database
from acutis_api.infrastructure.services.itau import ItauPixService

ROTA = '/api/admin/campanhas/registrar-campanha'


def test_registrar_campanha_cadastro_completa(
    client: FlaskClient, seed_registrar_membro, membro_token
):
    membro = seed_registrar_membro(status=True)[1]

    dados_da_campanha = {
        'nome': 'CAMPANHA PRE CADASTROS COMPLETO',
        'objetivo': 'cadastro',
        'publica': True,
        'ativa': True,
        'meta': 10000.0,
        'chave_pix': '123e4567-e89b-12d3-a456-426614174000',
        'criado_por': f'{membro.id}',
        'nome_campo': 'Telefone',
        'tipo_campo': 'string',
        'obrigatorio': True,
        'fk_cargo_oficial_id': None,
    }

    campos_adicionais = [
        {'nome_campo': 'tem não', 'tipo_campo': 'int', 'obrigatorio': True},
        {
            'nome_campo': 'data_nascimento',
            'tipo_campo': 'date',
            'obrigatorio': True,
        },
        {'nome_campo': 'email', 'tipo_campo': 'string', 'obrigatorio': True},
        {
            'nome_campo': 'status_ativo',
            'tipo_campo': 'string',
            'obrigatorio': True,
        },
    ]

    foto = (BytesIO(b'foto teste'), 'foto_teste.png')

    response = client.post(
        ROTA,
        headers={'Authorization': f'Bearer {membro_token}'},
        data={
            'foto_capa': foto,
            'campos_adicionais': json.dumps(campos_adicionais),
            'dados_da_campanha': json.dumps(dados_da_campanha),
        },
        content_type='multipart/form-data',
    )

    verificar_campanha_criada = (
        database.session.query(Campanha)
        .filter(Campanha.id == response.get_json().get('id'))
        .first()
    )

    assert response.status_code == HTTPStatus.CREATED
    assert verificar_campanha_criada is not None
    assert verificar_campanha_criada.nome == dados_da_campanha.get('nome')

    assert 'nome' in response.get_json().keys()
    assert 'id' in response.get_json().keys()


def test_registrar_campanha_cadastro_completa_sem_foto_campos_adicionais(
    client: FlaskClient, seed_registrar_membro, membro_token
):
    membro = seed_registrar_membro(status=True)[1]

    dados_da_campanha = {
        'nome': 'CAMPANHA CADASTROS',
        'objetivo': 'pre_cadastro',
        'publica': True,
        'ativa': True,
        'meta': 10000.0,
        'chave_pix': '123e4567-e89b-12d3-a456-426614174000',
        'criado_por': f'{membro.id}',
        'nome_campo': 'Telefone',
        'tipo_campo': 'string',
        'obrigatorio': True,
        'fk_cargo_oficial_id': None,
    }

    response = client.post(
        ROTA,
        headers={'Authorization': f'Bearer {membro_token}'},
        data={
            'dados_da_campanha': json.dumps(dados_da_campanha),
        },
        content_type='multipart/form-data',
    )

    verificar_campanha_criada = (
        database.session.query(Campanha)
        .filter(Campanha.id == response.get_json().get('id'))
        .first()
    )

    assert response.status_code == HTTPStatus.CREATED
    assert verificar_campanha_criada is not None
    assert verificar_campanha_criada.nome == dados_da_campanha.get('nome')

    assert 'nome' in response.get_json().keys()
    assert 'id' in response.get_json().keys()


@patch.object(ItauPixService, 'registrar_chave_pix_webhook')
def test_registrar_campanha_doacao(
    mock_registrar_chave_pix_webhook, client: FlaskClient, membro_token
):
    mock_registrar_chave_pix_webhook.return_value

    dados_da_campanha = {
        'nome': 'CAMPANHA DOACAO',
        'objetivo': 'doacao',
        'publica': True,
        'ativa': True,
        'meta': 10000.0,
        'chave_pix': '123e4567-e89b-12d3-a456-426614174000',
        'fk_cargo_oficial_id': None,
    }

    response = client.post(
        ROTA,
        headers={'Authorization': f'Bearer {membro_token}'},
        data={
            'dados_da_campanha': json.dumps(dados_da_campanha),
        },
        content_type='multipart/form-data',
    )

    verificar_campanha_criada = (
        database.session.query(Campanha)
        .filter(Campanha.id == response.get_json().get('id'))
        .first()
    )

    assert response.status_code == HTTPStatus.CREATED
    assert verificar_campanha_criada is not None
    assert verificar_campanha_criada.nome == dados_da_campanha.get('nome')

    assert 'nome' in response.get_json().keys()
    assert 'id' in response.get_json().keys()


def test_registrar_campanha_doacao_bad_request(
    client: FlaskClient, membro_token
):
    dados_da_campanha = {
        'nome': 'CAMPANHA DOACAO',
        'objetivo': 'doacao',
        'publica': True,
        'ativa': True,
        'meta': 10000.0,
        'chave_pix': '123e4567-e89b-12d3-a456-426614174000',
        'fk_cargo_oficial_id': None,
    }

    response = client.post(
        ROTA,
        headers={'Authorization': f'Bearer {membro_token}'},
        data={
            'dados_da_campanha': str(dados_da_campanha),  # request inválida
        },
        content_type='multipart/form-data',
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.get_json()[0]['msg'] == (
        'Value error, O campos devem conter um JSON válido.'
    )


def test_registrar_campanha_membro_oficial_completa_success(
    client: FlaskClient,
    seed_registrar_membro,
    membro_token,
    seed_cargo_oficial,
):
    cargo_oficial = seed_cargo_oficial

    membro = seed_registrar_membro(status=True)[1]

    dados_da_campanha = {
        'nome': 'CAMPANHA General',
        'objetivo': 'oficiais',
        'publica': True,
        'ativa': True,
        'meta': 10000.0,
        'chave_pix': None,
        'criado_por': f'{membro.id}',
        'fk_cargo_oficial_id': f'{cargo_oficial.id}',
    }

    campos_adicionais = [
        {'nome_campo': 'idade', 'tipo_campo': 'int', 'obrigatorio': True},
        {
            'nome_campo': 'conversão_em',
            'tipo_campo': 'date',
            'obrigatorio': True,
        },
        {'nome_campo': 'email', 'tipo_campo': 'string', 'obrigatorio': True},
        {'nome_campo': 'ativo', 'tipo_campo': 'int', 'obrigatorio': True},
    ]

    foto = (BytesIO(b'foto teste'), 'foto_teste.png')

    response = client.post(
        ROTA,
        headers={'Authorization': f'Bearer {membro_token}'},
        data={
            'foto_capa': foto,
            'campos_adicionais': json.dumps(campos_adicionais),
            'dados_da_campanha': json.dumps(dados_da_campanha),
        },
        content_type='multipart/form-data',
    )

    assert response.status_code == HTTPStatus.CREATED

    verificar_campanha_criada = (
        database.session.query(Campanha)
        .filter(Campanha.id == response.get_json().get('id'))
        .first()
    )

    assert verificar_campanha_criada is not None
    assert verificar_campanha_criada.nome == dados_da_campanha.get('nome')

    assert 'nome' in response.get_json().keys()
    assert 'id' in response.get_json().keys()


def test_registrar_campanha_membro_oficial_completa_bad_request_error(
    client: FlaskClient,
    seed_registrar_membro,
    membro_token,
    seed_cargo_oficial,
):
    membro = seed_registrar_membro(status=True)[1]

    dados_da_campanha = {
        'nome': 'CAMPANHA General',
        'objetivo': 'oficiais',
        'publica': True,
        'ativa': True,
        'meta': 10000.0,
        'chave_pix': None,
        'criado_por': f'{membro.id}',
        'fk_cargo_oficial_id': None,
    }

    campos_adicionais = [
        {'nome_campo': 'idade', 'tipo_campo': 'int', 'obrigatorio': True},
        {
            'nome_campo': 'conversão_em',
            'tipo_campo': 'date',
            'obrigatorio': True,
        },
        {'nome_campo': 'email', 'tipo_campo': 'string', 'obrigatorio': True},
        {'nome_campo': 'ativo', 'tipo_campo': 'int', 'obrigatorio': True},
    ]

    foto = (BytesIO(b'foto teste'), 'foto_teste.png')

    response = client.post(
        ROTA,
        headers={'Authorization': f'Bearer {membro_token}'},
        data={
            'foto_capa': foto,
            'campos_adicionais': json.dumps(campos_adicionais),
            'dados_da_campanha': json.dumps(dados_da_campanha),
        },
        content_type='multipart/form-data',
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    data = response.get_json()

    assert data == [{'msg': 'Deve ser informado um cargo oficial.'}]


def test_registrar_campanha_membro_oficial_sem_campos_adicionais_e_foto(
    client: FlaskClient,
    seed_registrar_membro,
    membro_token,
    seed_cargo_oficial,
):
    cargo_oficial = seed_cargo_oficial

    membro = seed_registrar_membro(status=True)[1]

    dados_da_campanha = {
        'nome': 'CAMPANHA General',
        'objetivo': 'oficiais',
        'publica': True,
        'ativa': True,
        'meta': 10000.0,
        'chave_pix': None,
        'criado_por': f'{membro.id}',
        'fk_cargo_oficial_id': f'{cargo_oficial.id}',
    }

    response = client.post(
        ROTA,
        headers={'Authorization': f'Bearer {membro_token}'},
        data={
            'dados_da_campanha': json.dumps(dados_da_campanha),
        },
        content_type='multipart/form-data',
    )

    assert response.status_code == HTTPStatus.CREATED

    verificar_campanha_criada = (
        database.session.query(Campanha)
        .filter(Campanha.id == response.get_json().get('id'))
        .first()
    )

    assert verificar_campanha_criada is not None
    assert verificar_campanha_criada.nome == dados_da_campanha.get('nome')

    assert 'nome' in response.get_json().keys()
    assert 'id' in response.get_json().keys()


def test_registra_campanha_com_nome_ja_cadastrado(
    client: FlaskClient, membro_token, seed_campanha_cadastro
):
    campanha_cadastrada = seed_campanha_cadastro

    dados_da_campanha = {
        'nome': f'{campanha_cadastrada.nome}',
        'objetivo': 'doacao',
        'publica': True,
        'ativa': True,
        'meta': 10000.0,
        'chave_pix': '123e4567-e89b-12d3-a456-426614174000',
        'fk_cargo_oficial_id': None,
    }

    response = client.post(
        ROTA,
        headers={'Authorization': f'Bearer {membro_token}'},
        data={
            'dados_da_campanha': json.dumps(dados_da_campanha),
        },
        content_type='multipart/form-data',
    )

    assert response.status_code == HTTPStatus.CONFLICT

    assert response.get_json() == [{'msg': 'Nome de campanha já cadastrado'}]
