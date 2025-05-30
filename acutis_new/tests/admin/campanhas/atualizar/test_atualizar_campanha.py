import json
import uuid
from http import HTTPStatus
from io import BytesIO
from unittest.mock import patch

from flask.testing import FlaskClient

from acutis_api.domain.entities.campanha import Campanha, ObjetivosCampanhaEnum
from acutis_api.domain.entities.campo_adicional import CampoAdicional
from acutis_api.infrastructure.extensions import database
from acutis_api.infrastructure.services.itau import ItauPixService

ROTA = '/api/admin/campanhas/atualizar-campanha'


@patch.object(ItauPixService, 'deletar_chave_pix_webhook')
@patch.object(ItauPixService, 'registrar_chave_pix_webhook')
def test_atualizar_campanha_doacao(
    mock_deletar_chave,
    mock_registrar_chave,
    client: FlaskClient,
    membro_token,
    seed_campanha_doacao,
):
    mock_deletar_chave.return_value
    mock_registrar_chave.return_value

    dados_da_campanha = {
        'nome': 'CAMPANHA DA MANGA',
        'objetivo': 'doacao',
        'publica': True,
        'ativa': True,
        'meta': 10000.0,
        'chave_pix': '123e4567-e89b-12d3-a456-426614174000',
        'fk_cargo_oficial_id': None,
    }

    response = client.put(
        f'{ROTA}/{seed_campanha_doacao.id}',
        headers={'Authorization': f'Bearer {membro_token}'},
        data={
            'dados_da_campanha': json.dumps(dados_da_campanha),
        },
        content_type='multipart/form-data',  # NOSONAR
    )

    assert response.status_code == HTTPStatus.OK
    verificar_atualizacao = database.session.query(Campanha).get(
        seed_campanha_doacao.id
    )
    assert verificar_atualizacao.nome == dados_da_campanha['nome']
    assert verificar_atualizacao.meta == dados_da_campanha['meta']
    assert verificar_atualizacao.publica == dados_da_campanha['publica']
    assert verificar_atualizacao.ativa == dados_da_campanha['ativa']
    assert verificar_atualizacao.chave_pix == dados_da_campanha['chave_pix']
    assert (
        verificar_atualizacao.fk_cargo_oficial_id
        == dados_da_campanha['fk_cargo_oficial_id']
    )


def test_atualizar_campanha_para_precadastro(
    client: FlaskClient, membro_token, seed_campanha_cadastro
):
    campanha_cadastro = seed_campanha_cadastro

    dados_da_campanha = {
        'nome': 'CAMPANHA DE PRÉ-CADASTRO',
        'objetivo': 'pre_cadastro',
        'publica': True,
        'ativa': True,
        'meta': 5000.0,
        'chave_pix': '123e4567-e89b-12d3-a456-426614174000',
        'fk_cargo_oficial_id': None,
    }

    imagem = (BytesIO(b'fake image data'), 'foto_campanha.jpg')  # NOSONAR

    response = client.put(
        f'{ROTA}/{campanha_cadastro.id}',
        headers={'Authorization': f'Bearer {membro_token}'},
        data={
            'dados_da_campanha': json.dumps(dados_da_campanha),
            'foto': imagem,
        },
        content_type='multipart/form-data',
    )

    assert response.status_code == HTTPStatus.OK

    verificar_atualizacao = database.session.query(Campanha).get(
        seed_campanha_cadastro.id
    )
    assert verificar_atualizacao.nome == dados_da_campanha['nome']
    assert verificar_atualizacao.meta == dados_da_campanha['meta']
    assert verificar_atualizacao.publica == dados_da_campanha['publica']
    assert verificar_atualizacao.ativa == dados_da_campanha['ativa']
    assert verificar_atualizacao.chave_pix == dados_da_campanha['chave_pix']


def test_atualizar_campanha_pre_cadastro_com_landing_page_sem_foto(
    client: FlaskClient,
    membro_token,
    seed_campanha_pre_cadastro_com_landing_page,
):
    campanha_pre_cadastro = seed_campanha_pre_cadastro_com_landing_page

    dados_da_campanha = {
        'nome': 'CAMPANHA DE PRÉ-CADASTRO ATUALIZADA',
        'objetivo': 'pre_cadastro',
        'publica': True,
        'ativa': True,
        'meta': 15000.0,
        'chave_pix': '123e4567-e89b-12d3-a456-426614174000',
        'fk_cargo_oficial_id': None,
    }

    response = client.put(
        f'{ROTA}/{campanha_pre_cadastro.id}',
        headers={'Authorization': f'Bearer {membro_token}'},
        data={
            'dados_da_campanha': json.dumps(dados_da_campanha),
        },
        content_type='multipart/form-data',
    )

    assert response.status_code == HTTPStatus.OK

    assert (
        seed_campanha_pre_cadastro_com_landing_page.nome
        == dados_da_campanha['nome']
    )
    assert (
        seed_campanha_pre_cadastro_com_landing_page.meta
        == dados_da_campanha['meta']
    )
    assert (
        seed_campanha_pre_cadastro_com_landing_page.publica
        == dados_da_campanha['publica']
    )
    assert (
        seed_campanha_pre_cadastro_com_landing_page.ativa
        == dados_da_campanha['ativa']
    )
    assert (
        seed_campanha_pre_cadastro_com_landing_page.chave_pix
        == dados_da_campanha['chave_pix']
    )


def test_atualizar_campanha_nome_ja_existente(
    client: FlaskClient,
    membro_token,
    seed_campanha_cadastro,
    seed_campanha_doacao,
):
    campanha_cadastro = seed_campanha_cadastro

    dados_da_campanha = {
        'nome': f'{seed_campanha_doacao.nome}',
        'objetivo': 'pre_cadastro',
        'publica': True,
        'ativa': True,
        'meta': 5000.0,
        'chave_pix': '123e4567-e89b-12d3-a456-426614174000',
        'fk_cargo_oficial_id': None,
    }

    imagem = (BytesIO(b'fake image data'), 'foto_campanha.jpg')

    response = client.put(
        f'{ROTA}/{campanha_cadastro.id}',
        headers={'Authorization': f'Bearer {membro_token}'},
        data={
            'dados_da_campanha': json.dumps(dados_da_campanha),
            'foto': imagem,
        },
        content_type='multipart/form-data',
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.get_json() == [{'msg': 'Nome de campanha já cadastrado'}]


def test_atualizar_campanha_membros_oficiais_bad_request(
    client: FlaskClient, membro_token, seed_campanha_membros_oficiais
):
    atualizar_campanha = seed_campanha_membros_oficiais

    dados_da_campanha = {
        'nome': 'CAMPANHA DE PRÉ-CADASTRO',
        'objetivo': 'oficiais',
        'publica': True,
        'ativa': True,
        'meta': 5000.0,
        'chave_pix': '123e4567-e89b-12d3-a456-426614174000',
        'fk_cargo_oficial_id': None,
    }

    imagem = (BytesIO(b'fake image data'), 'foto_campanha.jpg')

    response = client.put(
        f'{ROTA}/{atualizar_campanha.id}',
        headers={'Authorization': f'Bearer {membro_token}'},
        data={
            'dados_da_campanha': json.dumps(dados_da_campanha),
            'foto': imagem,
        },
        content_type='multipart/form-data',
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.get_json() == [
        {'msg': 'Deve ser informado um cargo oficial.'}
    ]


def test_atualizar_campanha_membros_oficiais_sucess(
    client: FlaskClient, membro_token, seed_campanha_membros_oficiais
):
    atualizar_campanha = seed_campanha_membros_oficiais

    dados_da_campanha = {
        'nome': 'CAMPANHA DE Oficiais',
        'objetivo': 'oficiais',
        'publica': True,
        'ativa': True,
        'meta': 5000.0,
        'chave_pix': '123e4567-e89b-12d3-a456-426614174000',
        'fk_cargo_oficial_id': str(atualizar_campanha.fk_cargo_oficial_id),
    }

    imagem = (BytesIO(b'fake image data'), 'foto_campanha.jpg')

    response = client.put(
        f'{ROTA}/{atualizar_campanha.id}',
        headers={'Authorization': f'Bearer {membro_token}'},
        data={
            'dados_da_campanha': json.dumps(dados_da_campanha),
            'foto': imagem,
        },
        content_type='multipart/form-data',
    )

    assert response.status_code == HTTPStatus.OK
    assert seed_campanha_membros_oficiais.nome == dados_da_campanha['nome']
    assert seed_campanha_membros_oficiais.meta == dados_da_campanha['meta']
    assert (
        seed_campanha_membros_oficiais.publica == dados_da_campanha['publica']
    )
    assert seed_campanha_membros_oficiais.ativa == dados_da_campanha['ativa']
    assert (
        seed_campanha_membros_oficiais.chave_pix
        == dados_da_campanha['chave_pix']
    )


def test_atualizar_campanha_nao_existente(client: FlaskClient, membro_token):
    atualizar_campanha = uuid.uuid4()

    dados_da_campanha = {
        'nome': 'campanha não existente',
        'objetivo': 'doacao',
        'publica': True,
        'ativa': True,
        'meta': 5000.0,
        'chave_pix': '123e4567-e89b-12d3-a456-426614174000',
        'fk_cargo_oficial_id': None,
    }

    response = client.put(
        f'{ROTA}/{atualizar_campanha}',
        headers={'Authorization': f'Bearer {membro_token}'},
        data={
            'dados_da_campanha': json.dumps(dados_da_campanha),
        },
        content_type='multipart/form-data',
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.get_json() == [{'msg': 'Campanha não encontrada'}]


@patch.object(ItauPixService, 'deletar_chave_pix_webhook')
@patch.object(ItauPixService, 'registrar_chave_pix_webhook')
def test_atualizar_obrigatoriedade_campos_adicionais(
    mock_deletar_chave,
    mock_registrar_chave,
    client: FlaskClient,
    membro_token,
    seed_nova_campanha_com_campos_adicionais,
):
    mock_deletar_chave.return_value
    mock_registrar_chave.return_value

    campanha, campos = seed_nova_campanha_com_campos_adicionais(
        [
            {'tipo_campo': 'string', 'obrigatorio': True},
            {'tipo_campo': 'int', 'obrigatorio': False},
        ],
        objetivo_campanha=ObjetivosCampanhaEnum.doacao,
    )

    nome_campo1 = campos[0].nome_campo
    nome_campo2 = campos[1].nome_campo

    payload = {
        'dados_da_campanha': json.dumps({
            'nome': 'Campanha atualizada',
            'objetivo': 'doacao',
            'publica': True,
            'ativa': True,
            'meta': 5000.0,
            'chave_pix': '123e4567-e89b-12d3-a456-426614174000',
            'fk_cargo_oficial_id': None,
        }),
        'campos_adicionais': json.dumps([
            {
                'nome_campo': nome_campo1,
                'tipo_campo': 'string',
                'valor_campo': 'valor1',
                'obrigatorio': False,  # Invertendo
            },
            {
                'nome_campo': nome_campo2,
                'tipo_campo': 'int',
                'valor_campo': '123',
                'obrigatorio': True,  # Invertendo
            },
        ]),
    }

    response = client.put(
        f'{ROTA}/{campanha.id}',
        headers={'Authorization': f'Bearer {membro_token}'},
        data=payload,
        content_type='multipart/form-data',
    )

    campo1 = (
        database.session.query(CampoAdicional)
        .filter_by(nome_campo=nome_campo1, fk_campanha_id=campanha.id)
        .first()
    )

    campo2 = (
        database.session.query(CampoAdicional)
        .filter_by(nome_campo=nome_campo2, fk_campanha_id=campanha.id)
        .first()
    )

    assert response.status_code == HTTPStatus.OK
    assert campo1.obrigatorio is False
    assert campo2.obrigatorio is True


@patch.object(ItauPixService, 'deletar_chave_pix_webhook')
@patch.object(ItauPixService, 'registrar_chave_pix_webhook')
def test_campos_adicionais_inexistentes_sao_ignorados(
    mock_deletar_chave,
    mock_registrar_chave,
    client: FlaskClient,
    membro_token,
    seed_nova_campanha_com_campos_adicionais,
):
    mock_deletar_chave.return_value
    mock_registrar_chave.return_value

    campanha, campos = seed_nova_campanha_com_campos_adicionais(
        [],
        objetivo_campanha=ObjetivosCampanhaEnum.doacao,
    )

    payload = {
        'dados_da_campanha': json.dumps({
            'nome': 'Campanha campo inexistente',
            'objetivo': 'doacao',
            'publica': True,
            'ativa': True,
            'meta': 5000.0,
            'chave_pix': '123e4567-e89b-12d3-a456-426614174000',
            'fk_cargo_oficial_id': None,
        }),
        'campos_adicionais': json.dumps([
            {
                'nome_campo': 'campo_inexistente',
                'tipo_campo': 'string',
                'valor_campo': 'valor',
                'obrigatorio': True,
            }
        ]),
    }

    response = client.put(
        f'{ROTA}/{campanha.id}',
        headers={'Authorization': f'Bearer {membro_token}'},
        data=payload,
        content_type='multipart/form-data',
    )

    assert response.status_code == HTTPStatus.OK
    assert (
        database.session.query(CampoAdicional)
        .filter_by(fk_campanha_id=campanha.id)
        .count()
        == 0
    )


@patch.object(ItauPixService, 'deletar_chave_pix_webhook')
@patch.object(ItauPixService, 'registrar_chave_pix_webhook')
def test_atualizar_campanha_com_nova_foto_capa(
    mock_deletar_chave,
    mock_registrar_chave,
    client: FlaskClient,
    membro_token,
    seed_campanha_doacao,
):
    mock_deletar_chave.return_value
    mock_registrar_chave.return_value

    imagem = (BytesIO(b'fake image data'), 'foto_capa.jpg')

    dados_da_campanha = {
        'nome': 'Campanha com nova foto',
        'objetivo': 'doacao',
        'publica': True,
        'ativa': True,
        'meta': 5000.0,
        'chave_pix': '123e4567-e89b-12d3-a456-426614174000',
        'fk_cargo_oficial_id': None,
    }

    response = client.put(
        f'{ROTA}/{seed_campanha_doacao.id}',
        headers={'Authorization': f'Bearer {membro_token}'},
        data={
            'dados_da_campanha': json.dumps(dados_da_campanha),
            'foto_capa': imagem,
        },
        content_type='multipart/form-data',
    )

    assert response.status_code == HTTPStatus.OK

    campanha_atualizada = database.session.query(Campanha).get(
        seed_campanha_doacao.id
    )
    assert campanha_atualizada.capa is not None
