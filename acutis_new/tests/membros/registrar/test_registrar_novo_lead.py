import base64
import io
import uuid
from http import HTTPStatus

import pytest
from flask.testing import FlaskClient
from PIL import Image

from acutis_api.domain.entities.campo_adicional import TiposCampoEnum
from acutis_api.domain.entities.lead import Lead
from acutis_api.infrastructure.extensions import database
from tests.factories import (
    LeadFactory,
)

ROTA_REGISTRAR_NOVO_LEAD = '/api/membros/registrar-novo-lead'
SENHA_TESTE = '#Teste@1234'


def test_registrar_novo_lead_sucesso(client: FlaskClient, seed_nova_campanha):
    campanha = seed_nova_campanha()

    payload = {
        'nome': 'lead test',
        'email': 'leadteste@gmail.com',
        'telefone': '85998685421',
        'pais': 'brasil',
        'campanha_id': campanha.id,
        'origem_cadastro': 'acutis',
    }

    response = client.post(ROTA_REGISTRAR_NOVO_LEAD, json=payload)

    assert response.status_code == HTTPStatus.CREATED
    response_json = response.json
    assert 'id' in response_json
    assert 'nome' in response_json
    lead = database.session.get(Lead, response_json['id'])
    assert lead is not None


def test_registrar_novo_lead_erro_email_ja_cadastrado(
    client: FlaskClient, seed_nova_campanha
):
    campanha = seed_nova_campanha()

    lead = LeadFactory()
    lead.senha = SENHA_TESTE
    database.session.add(lead)
    database.session.commit()

    payload = {
        'nome': 'lead teste',
        'email': lead.email,
        'telefone': '85998685421',
        'pais': 'brasil',
        'campanha_id': campanha.id,
        'origem_cadastro': 'acutis',
        'senha': SENHA_TESTE,
    }

    response = client.post(ROTA_REGISTRAR_NOVO_LEAD, json=payload)

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json == [{'msg': 'Ops, email já cadastrado.'}]


def test_registrar_novo_lead_com_campanha_campos_adicionais_sucesso(
    client: FlaskClient, seed_nova_campanha_com_campos_adicionais
):
    tipos_campos_adicionais = [
        {'tipo_campo': 'date', 'obrigatorio': True},
        {'tipo_campo': 'arquivo', 'obrigatorio': True},
    ]
    campanha, campos_adicionais = seed_nova_campanha_com_campos_adicionais(
        tipos_campos_adicionais
    )

    imagem = Image.new('RGB', (100, 100), color=(255, 0, 0))
    buff = io.BytesIO()
    imagem.save(buff, format='JPEG')
    buff.seek(0)

    imagem_base64 = base64.b64encode(buff.getvalue()).decode('utf-8')
    base64_string = f'data:image/jpeg;base64,{imagem_base64}'

    payload = {
        'nome': 'Lead Teste a',
        'email': 'leadteste1@headers.com.br',
        'telefone': '85986821142',
        'pais': 'brasil',
        'campanha_id': campanha.id,
        'origem_cadastro': 'acutis',
        'campos_adicionais': [
            {
                'campo_adicional_id': campos_adicionais[0].id,
                'valor_campo': '1998-01-21',
            },
            {
                'campo_adicional_id': campos_adicionais[1].id,
                'valor_campo': base64_string,
            },
        ],
    }

    response = client.post(ROTA_REGISTRAR_NOVO_LEAD, json=payload)

    assert response.status_code == HTTPStatus.CREATED
    response_json = response.json
    assert 'id' in response_json
    assert response_json['nome'] == payload['nome'].title()


def test_registrar_novo_lead_erro_campanha_nao_encontrada(client: FlaskClient):
    payload = {
        'nome': 'lead teste',
        'email': 'emaillead@gmail.com',
        'telefone': '85998685421',
        'pais': 'brasil',
        'campanha_id': str(uuid.uuid4()),
        'origem_cadastro': 'acutis',
        'senha': SENHA_TESTE,
    }

    response = client.post(ROTA_REGISTRAR_NOVO_LEAD, json=payload)

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json == [{'msg': 'Ops, Campanha não encontrada.'}]


def test_registrar_novo_lead_erro_campanha_inativa(
    client: FlaskClient, seed_nova_campanha
):
    campanha = seed_nova_campanha(ativa=False)

    payload = {
        'nome': 'lead teste y',
        'email': 'emaillead2@gmail.com',
        'telefone': '85998685421',
        'pais': 'brasil',
        'campanha_id': campanha.id,
        'origem_cadastro': 'acutis',
        'senha': SENHA_TESTE,
    }

    response = client.post(ROTA_REGISTRAR_NOVO_LEAD, json=payload)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json == [
        {'msg': 'Ops, a campanha está inativa e não pode receber cadastros.'}
    ]


def test_registrar_novo_lead_erro_campo_faltante_payload(
    client: FlaskClient, seed_nova_campanha_com_campos_adicionais
):
    tipos_campos_adicionais = [
        {'tipo_campo': 'float', 'obrigatorio': True},
    ]
    campanha, _ = seed_nova_campanha_com_campos_adicionais(
        tipos_campos_adicionais
    )

    payload = {
        'nome': 'Lead Teste t',
        'email': 'leadteste2@headers.com.br',
        'telefone': '85986821142',
        'pais': 'brasil',
        'campanha_id': campanha.id,
        'origem_cadastro': 'acutis',
        'senha': SENHA_TESTE,
        'campos_adicionais': [],
    }

    response = client.post(ROTA_REGISTRAR_NOVO_LEAD, json=payload)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json == [
        {'msg': 'Campos obrigatórios faltantes na campanha.'}
    ]


def test_registrar_novo_lead_erro_campo_adicional_invalido_payload(
    client: FlaskClient, seed_nova_campanha_com_campos_adicionais
):
    tipos_campos_adicionais = [
        {'tipo_campo': 'integer', 'obrigatorio': True},
    ]
    campanha, campos_adicionais = seed_nova_campanha_com_campos_adicionais(
        tipos_campos_adicionais
    )

    payload = {
        'nome': 'Lead Teste',
        'email': 'leadteste@headers.com.br',
        'telefone': '85986821142',
        'pais': 'brasil',
        'campanha_id': campanha.id,
        'origem_cadastro': 'acutis',
        'senha': SENHA_TESTE,
        'campos_adicionais': [
            {
                'campo_adicional_id': campos_adicionais[0].id,
                'valor_campo': 10,
            },
            {
                'campo_adicional_id': '90af9c45-59e1-439d-aeb8-598ef7a6a982',
                'valor_campo': 50,
            },
        ],
    }

    response = client.post(ROTA_REGISTRAR_NOVO_LEAD, json=payload)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json == [{'msg': 'Campo adicional inválido.'}]


@pytest.mark.parametrize(
    ('tipo_campo', 'valor_campo', 'msg_erro'),
    [
        (
            TiposCampoEnum.string,
            ['definitivamente nao sou do tipo string'],
            'O campo "{0}" deve ser uma string.',
        ),
        (
            TiposCampoEnum.integer,
            'teste',
            'O campo "{0}" deve ser um número inteiro.',
        ),
        (
            TiposCampoEnum.float,
            'YYYY-MM-DD',
            'O campo "{0}" deve ser um número decimal.',
        ),
        (
            TiposCampoEnum.date,
            77,
            'O campo "{0}" deve estar no formato YYYY-MM-DD.',
        ),
        (
            TiposCampoEnum.datetime,
            'любопытный',
            'O campo "{0}" deve estar no formato ISO 8601.',
        ),
        (
            TiposCampoEnum.arquivo,
            'não é base meia quatro',
            'Ops, o Base64 enviado é inválido.',
        ),
        (
            TiposCampoEnum.arquivo,
            'data:',
            'Ops, não foi possível decodificar o Base64.',
        ),
    ],
)
def test_registrar_novo_lead_erros_validacoes_tipo_campos_adicionais(
    tipo_campo,
    valor_campo,
    msg_erro,
    client: FlaskClient,
    seed_nova_campanha_com_campos_adicionais,
):
    tipos_campos_adicionais = [
        {'tipo_campo': tipo_campo, 'obrigatorio': True},
    ]
    campanha, campos_adicionais = seed_nova_campanha_com_campos_adicionais(
        tipos_campos_adicionais
    )

    payload = {
        'nome': 'Lead Teste',
        'email': 'leadteste@headers.com.br',
        'telefone': '85986821142',
        'pais': 'brasil',
        'campanha_id': campanha.id,
        'origem_cadastro': 'acutis',
        'senha': SENHA_TESTE,
        'campos_adicionais': [
            {
                'campo_adicional_id': campos_adicionais[0].id,
                'valor_campo': valor_campo,
            },
        ],
    }

    response = client.post(ROTA_REGISTRAR_NOVO_LEAD, json=payload)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json == [
        {'msg': msg_erro.format(campos_adicionais[0].nome_campo)}
    ]
