import base64
import io
import json
from http import HTTPStatus
from io import BytesIO

import pytest
from faker import Faker
from flask.testing import FlaskClient
from PIL import Image
from werkzeug.datastructures import FileStorage

from acutis_api.communication.enums.campanhas import ObjetivosCampanhaEnum
from acutis_api.communication.enums.membros import OrigemCadastroEnum, SexoEnum
from acutis_api.domain.entities.lead import Lead
from acutis_api.domain.entities.membro import Membro
from acutis_api.domain.entities.oficial import Oficial
from acutis_api.infrastructure.extensions import database
from tests.factories import (
    CampanhaFactory,
    CampanhaMembroOficialFactory,
    CampoAdicionalFactory,
    CargosOficiaisFactory,
    LeadFactory,
)

faker = Faker('pt-BR')


def gerar_imagem_base64():
    imagem = Image.new('RGB', (100, 100), color=(255, 0, 0))
    buff = io.BytesIO()
    imagem.save(buff, format='JPEG')
    buff.seek(0)
    return f'data:image/jpeg;base64,{
        base64.b64encode(buff.getvalue()).decode("utf-8")
    }'


@pytest.fixture
def mock_image_file():
    return BytesIO(b'fake image data'), 'test_image.jpg'


def test_cadastro_por_campanha_vincula_oficial(
    client: FlaskClient,
    seed_registrar_membro,
    seed_membros_oficial,
    seed_cargo_oficial,
):
    lead, membro, _ = seed_registrar_membro(status=True)

    superior = seed_membros_oficial[0]

    cargo_oficial = seed_cargo_oficial

    membro_oficial = Oficial(
        fk_membro_id=membro.id,
        fk_superior_id=superior.fk_membro_id,
        fk_cargo_oficial_id=cargo_oficial.id,
        status='aprovado',
        atualizado_por=None,
    )

    database.session.add(membro_oficial)
    database.session.commit()

    cargo_oficial = CargosOficiaisFactory(criado_por=membro.id)

    database.session.add(cargo_oficial)
    database.session.commit()

    campanha_oficiais = CampanhaMembroOficialFactory(
        criado_por=membro.id, fk_cargo_oficial_id=cargo_oficial.id
    )
    database.session.add(campanha_oficiais)

    token = client.post(
        '/api/autenticacao/login?httponly=false',
        json={
            'email': lead.email,
            'senha': '#Teste;@123',
        },
    ).get_json()['access_token']

    response = client.post(
        f'/api/admin/campanhas/cadastro-por-campanha/{campanha_oficiais.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json == {
        'msg': 'Oficial vinculado a campanha com sucesso.'
    }


def test_cadastro_por_campanha_membro_logado_vira_oficial(
    client: FlaskClient,
    seed_registrar_membro,
    seed_membros_oficial,
):
    lead, membro, endereco = seed_registrar_membro(status=True)

    superior = seed_membros_oficial[0]

    cargo_oficial = CargosOficiaisFactory(criado_por=membro.id)

    database.session.add(cargo_oficial)
    database.session.commit()

    campanha_oficiais = CampanhaMembroOficialFactory(
        criado_por=membro.id, fk_cargo_oficial_id=cargo_oficial.id
    )
    database.session.add(campanha_oficiais)
    database.session.commit()

    tipos_campos_adicionais = [
        {'tipo_campo': 'date', 'obrigatorio': True},
        {'tipo_campo': 'arquivo', 'obrigatorio': False},
    ]

    campos_adicionais = []
    for campo in tipos_campos_adicionais:
        campo_adicional = CampoAdicionalFactory(
            fk_campanha_id=campanha_oficiais.id,
            tipo_campo=campo['tipo_campo'],
            obrigatorio=campo['obrigatorio'],
        )
        campos_adicionais.append(campo_adicional)
    database.session.add_all(campos_adicionais)
    database.session.commit()

    token = client.post(
        '/api/autenticacao/login?httponly=false',
        json={
            'email': lead.email,
            'senha': '#Teste;@123',
        },
    ).get_json()['access_token']

    imagem_base64 = gerar_imagem_base64()

    data = {
        'nome': 'Eric',
        'email': lead.email,
        'telefone': lead.telefone,
        'origem_cadastro': lead.origem_cadastro,
        'nome_social': 'Eric Gomes',
        'numero_documento': membro.numero_documento,
        'data_nascimento': membro.data_nascimento.strftime('%Y-%m-%d'),
        'sexo': membro.sexo,
        'superior': str(superior.fk_membro_id),
        'endereco': json.dumps({
            'codigo_postal': endereco.codigo_postal,
            'tipo_logradouro': endereco.tipo_logradouro,
            'logradouro': endereco.logradouro,
            'numero': endereco.numero,
            'complemento': endereco.complemento,
            'bairro': endereco.bairro,
            'cidade': endereco.cidade,
            'estado': 'PB',
            'pais': endereco.pais,
        }),
        'campos_adicionais': json.dumps([
            {
                'campo_adicional_id': str(campos_adicionais[0].id),
                'valor_campo': '1998-01-21',
            },
            {
                'campo_adicional_id': str(campos_adicionais[1].id),
                'valor_campo': imagem_base64,
            },
        ]),
    }

    response = client.post(
        f'/api/admin/campanhas/cadastro-por-campanha/{campanha_oficiais.id}',
        headers={'Authorization': f'Bearer {token}'},
        data=data,
        content_type='multipart/form-data',
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json == {'msg': 'Oficial cadastrado com sucesso.'}
    oficial_cadastrado = (
        database.session.query(Oficial)
        .filter(Oficial.fk_membro_id == membro.id)
        .first()
    )

    assert oficial_cadastrado.status == 'pendente'


def test_cadastro_por_campanha_lead_logado_vira_oficial(
    client: FlaskClient, seed_membros_oficial
):
    lead = LeadFactory(status=True)
    lead.senha = '#Teste;@123'
    database.session.add(lead)
    database.session.commit()

    superior = seed_membros_oficial[0]

    token = client.post(
        '/api/autenticacao/login?httponly=false',
        json={
            'email': lead.email,
            'senha': '#Teste;@123',
        },
    ).get_json()['access_token']

    cargo_oficial = CargosOficiaisFactory(criado_por=superior.fk_membro_id)

    database.session.add(cargo_oficial)
    database.session.commit()

    campanha_oficiais = CampanhaMembroOficialFactory(
        criado_por=superior.fk_membro_id, fk_cargo_oficial_id=cargo_oficial.id
    )
    database.session.add(campanha_oficiais)
    database.session.commit()

    tipos_campos_adicionais = [
        {'tipo_campo': 'date', 'obrigatorio': True},
        {'tipo_campo': 'arquivo', 'obrigatorio': False},
    ]

    campos_adicionais = []
    for campo in tipos_campos_adicionais:
        campo_adicional = CampoAdicionalFactory(
            fk_campanha_id=campanha_oficiais.id,
            tipo_campo=campo['tipo_campo'],
            obrigatorio=campo['obrigatorio'],
        )
        campos_adicionais.append(campo_adicional)
    database.session.add_all(campos_adicionais)
    database.session.commit()

    imagem_base64 = gerar_imagem_base64()

    data = {
        'nome': 'Eric',
        'email': lead.email,
        'telefone': lead.telefone,
        'origem_cadastro': lead.origem_cadastro,
        'nome_social': 'Eric Gomes',
        'numero_documento': '10144044485',
        'data_nascimento': '2003-01-21',
        'sexo': SexoEnum.masculino,
        'superior': str(superior.fk_membro_id),
        'endereco': json.dumps({
            'codigo_postal': '58053-022',
            'tipo_logradouro': 'Rua',
            'logradouro': 'José Firmino da Silva',
            'numero': '884',
            'complemento': 'Casa',
            'bairro': 'Jardim São Paulo',
            'cidade': 'João Pessoa',
            'estado': 'PB',
            'pais': 'brasil',
        }),
        'campos_adicionais': json.dumps([
            {
                'campo_adicional_id': str(campos_adicionais[0].id),
                'valor_campo': '1998-01-21',
            },
            {
                'campo_adicional_id': str(campos_adicionais[1].id),
                'valor_campo': imagem_base64,
            },
        ]),
    }

    response = client.post(
        f'/api/admin/campanhas/cadastro-por-campanha/{campanha_oficiais.id}',
        headers={'Authorization': f'Bearer {token}'},
        data=data,
        content_type='multipart/form-data',
    )

    assert response.json == {'msg': 'Oficial cadastrado com sucesso.'}
    assert response.status_code == HTTPStatus.CREATED
    oficial_cadastrado = (
        database.session.query(Oficial)
        .join(Membro, Oficial.fk_membro_id == Membro.id)
        .filter(Membro.fk_lead_id == lead.id)
        .first()
    )

    assert oficial_cadastrado.status == 'pendente'


def test_cadastro_por_campanha_adicionais_nao_enviados(
    client: FlaskClient,
    seed_registrar_membro,
    seed_campanha_membros_oficiais,
    seed_membros_oficial,
    seed_cargo_oficial,
):
    lead, membro, _ = seed_registrar_membro(status=True)

    campanha = seed_campanha_membros_oficiais

    superior = seed_membros_oficial[0]

    cargo_oficial = seed_cargo_oficial

    membro_oficial = Oficial(
        fk_membro_id=membro.id,
        fk_superior_id=superior.fk_membro_id,
        fk_cargo_oficial_id=cargo_oficial.id,
        status='aprovado',
        atualizado_por=None,
    )

    database.session.add(membro_oficial)
    database.session.commit()

    token = client.post(
        '/api/autenticacao/login?httponly=false',
        json={
            'email': lead.email,
            'senha': '#Teste;@123',
        },
    ).get_json()['access_token']

    response = client.post(
        f'/api/admin/campanhas/cadastro-por-campanha/{campanha.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json == [
        {'msg': 'É necessário informar os campos adicionais.'}
    ]


def test_cadastro_por_campanha_membro_logado_vincula(
    client: FlaskClient,
    seed_registrar_membro,
    seed_membros_oficial,
):
    lead, membro, endereco = seed_registrar_membro(status=True)

    superior = seed_membros_oficial[0]

    token = client.post(
        '/api/autenticacao/login?httponly=false',
        json={
            'email': lead.email,
            'senha': '#Teste;@123',
        },
    ).get_json()['access_token']

    campanha_cadastro = CampanhaFactory(
        objetivo=ObjetivosCampanhaEnum.cadastro,
        criado_por=superior.fk_membro_id,
    )
    database.session.add(campanha_cadastro)
    database.session.commit()

    tipos_campos_adicionais = [
        {'tipo_campo': 'date', 'obrigatorio': True},
        {'tipo_campo': 'float', 'obrigatorio': False},
    ]

    campos_adicionais = []
    for campo in tipos_campos_adicionais:
        campo_adicional = CampoAdicionalFactory(
            fk_campanha_id=campanha_cadastro.id,
            tipo_campo=campo['tipo_campo'],
            obrigatorio=campo['obrigatorio'],
        )
        campos_adicionais.append(campo_adicional)
    database.session.add_all(campos_adicionais)
    database.session.commit()

    data = {
        'nome': 'Eric',
        'email': lead.email,
        'telefone': lead.telefone,
        'origem_cadastro': lead.origem_cadastro,
        'nome_social': 'Eric Gomes',
        'numero_documento': membro.numero_documento,
        'data_nascimento': membro.data_nascimento.strftime('%Y-%m-%d'),
        'sexo': membro.sexo,
        'superior': str(superior.fk_membro_id),
        'endereco': json.dumps({
            'codigo_postal': endereco.codigo_postal,
            'tipo_logradouro': endereco.tipo_logradouro,
            'logradouro': endereco.logradouro,
            'numero': endereco.numero,
            'complemento': endereco.complemento,
            'bairro': endereco.bairro,
            'cidade': endereco.cidade,
            'estado': 'PB',
            'pais': endereco.pais,
        }),
        'campos_adicionais': json.dumps([
            {
                'campo_adicional_id': str(campos_adicionais[0].id),
                'valor_campo': '1998-01-21',
            },
            {
                'campo_adicional_id': str(campos_adicionais[1].id),
                'valor_campo': '15.00',
            },
        ]),
    }

    response = client.post(
        f'/api/admin/campanhas/cadastro-por-campanha/{campanha_cadastro.id}',
        headers={'Authorization': f'Bearer {token}'},
        data=data,
        content_type='multipart/form-data',
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json == {'msg': 'Membro vinculado a campanha com sucesso.'}


def test_cadastro_por_campanha_lead_logado_vira_membro(
    client: FlaskClient,
    seed_membros_oficial,
):
    lead = LeadFactory(status=True)
    lead.senha = '#Teste;@123'
    database.session.add(lead)
    database.session.commit()

    superior = seed_membros_oficial[0]

    token = client.post(
        '/api/autenticacao/login?httponly=false',
        json={
            'email': lead.email,
            'senha': '#Teste;@123',
        },
    ).get_json()['access_token']

    campanha_cadastro = CampanhaFactory(
        objetivo=ObjetivosCampanhaEnum.cadastro,
        criado_por=superior.fk_membro_id,
    )
    database.session.add(campanha_cadastro)
    database.session.commit()

    data = {
        'nome': 'Eric',
        'email': lead.email,
        'telefone': lead.telefone,
        'origem_cadastro': lead.origem_cadastro,
        'nome_social': 'Eric Gomes',
        'numero_documento': '888812345678',
        'data_nascimento': '2003-01-21',
        'sexo': SexoEnum.masculino,
        'superior': str(superior.fk_membro_id),
        'endereco': json.dumps({
            'codigo_postal': '58053-022',
            'tipo_logradouro': 'Rua',
            'logradouro': 'José Firmino da Silva',
            'numero': '884',
            'complemento': 'Casa',
            'bairro': 'Jardim São Paulo',
            'cidade': 'João Pessoa',
            'estado': 'PB',
            'pais': 'brasil',
        }),
    }

    response = client.post(
        f'/api/admin/campanhas/cadastro-por-campanha/{campanha_cadastro.id}',
        headers={'Authorization': f'Bearer {token}'},
        data=data,
        content_type='multipart/form-data',
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json == {'msg': 'Membro cadastrado com sucesso.'}


def test_cadastro_por_campanha_lead_logado_vincula(
    client: FlaskClient, seed_membros_oficial
):
    lead = LeadFactory(status=True)
    lead.senha = '#Teste;@123'
    database.session.add(lead)
    database.session.commit()

    superior = seed_membros_oficial[0]

    token = client.post(
        '/api/autenticacao/login?httponly=false',
        json={
            'email': lead.email,
            'senha': '#Teste;@123',
        },
    ).get_json()['access_token']

    campanha_lead = CampanhaFactory(
        objetivo=ObjetivosCampanhaEnum.pre_cadastro,
        criado_por=superior.fk_membro_id,
    )
    database.session.add(campanha_lead)
    database.session.commit()

    tipos_campos_adicionais = [
        {'tipo_campo': 'date', 'obrigatorio': True},
        {'tipo_campo': 'float', 'obrigatorio': False},
    ]

    campos_adicionais = []
    for campo in tipos_campos_adicionais:
        campo_adicional = CampoAdicionalFactory(
            fk_campanha_id=campanha_lead.id,
            tipo_campo=campo['tipo_campo'],
            obrigatorio=campo['obrigatorio'],
        )
        campos_adicionais.append(campo_adicional)
    database.session.add_all(campos_adicionais)
    database.session.commit()

    data = {
        'nome': 'Eric',
        'email': lead.email,
        'telefone': lead.telefone,
        'origem_cadastro': lead.origem_cadastro,
        'pais': lead.pais,
        'superior': str(superior.fk_membro_id),
        'campos_adicionais': json.dumps([
            {
                'campo_adicional_id': str(campos_adicionais[0].id),
                'valor_campo': '1998-01-21',
            },
            {
                'campo_adicional_id': str(campos_adicionais[1].id),
                'valor_campo': '15.00',
            },
        ]),
    }

    response = client.post(
        f'/api/admin/campanhas/cadastro-por-campanha/{campanha_lead.id}',
        headers={'Authorization': f'Bearer {token}'},
        data=data,
        content_type='multipart/form-data',
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json == {'msg': 'Lead vinculado a campanha com sucesso.'}


def test_cadastro_por_campanha_membro_oficial(
    client: FlaskClient, seed_membros_oficial, mock_image_file
):
    superior = seed_membros_oficial[0]

    cargo_oficial = CargosOficiaisFactory(criado_por=superior.fk_membro_id)

    database.session.add(cargo_oficial)
    database.session.commit()

    campanha_oficiais = CampanhaMembroOficialFactory(
        criado_por=superior.fk_membro_id, fk_cargo_oficial_id=cargo_oficial.id
    )
    database.session.add(campanha_oficiais)
    database.session.commit()

    tipos_campos_adicionais = [
        {'tipo_campo': 'date', 'obrigatorio': True},
        {'tipo_campo': 'arquivo', 'obrigatorio': False},
    ]

    campos_adicionais = []
    for campo in tipos_campos_adicionais:
        campo_adicional = CampoAdicionalFactory(
            fk_campanha_id=campanha_oficiais.id,
            tipo_campo=campo['tipo_campo'],
            obrigatorio=campo['obrigatorio'],
        )
        campos_adicionais.append(campo_adicional)
    database.session.add_all(campos_adicionais)
    database.session.commit()

    imagem_base64 = gerar_imagem_base64()

    mock_file, filename = mock_image_file
    file_storage = FileStorage(
        stream=mock_file, filename=filename, content_type='image/jpeg'
    )

    data = {
        'nome': 'Eric',
        'email': 'testando@email.com',
        'telefone': '85998685421',
        'origem_cadastro': OrigemCadastroEnum.acutis,
        'nome_social': 'Eric Gomes',
        'pais': 'brasil',
        'foto': (file_storage, filename),
        'numero_documento': '10144044485',
        'data_nascimento': '2003-01-21',
        'sexo': SexoEnum.masculino,
        'superior': str(superior.fk_membro_id),
        'senha': '#Teste;@123',
        'endereco': json.dumps({
            'codigo_postal': '58053-022',
            'tipo_logradouro': 'Rua',
            'logradouro': 'José Firmino da Silva',
            'numero': '884',
            'complemento': 'Casa',
            'bairro': 'Jardim São Paulo',
            'cidade': 'João Pessoa',
            'estado': 'PB',
            'pais': 'brasil',
        }),
        'campos_adicionais': json.dumps([
            {
                'campo_adicional_id': str(campos_adicionais[0].id),
                'valor_campo': '1998-01-21',
            },
            {
                'campo_adicional_id': str(campos_adicionais[1].id),
                'valor_campo': imagem_base64,
            },
        ]),
    }

    response = client.post(
        f'/api/admin/campanhas/cadastro-por-campanha/{campanha_oficiais.id}',
        data=data,
        content_type='multipart/form-data',
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json == {'msg': 'Oficial cadastrado com sucesso.'}
    oficial_cadastrado = (
        database.session.query(Oficial)
        .join(Membro, Oficial.fk_membro_id == Membro.id)
        .filter(Membro.numero_documento == '10144044485')
        .first()
    )

    assert oficial_cadastrado.status == 'pendente'


def test_cadastro_por_campanha_membro(
    client: FlaskClient,
    seed_membros_oficial,
):
    superior = seed_membros_oficial[0]

    campanha_cadastro = CampanhaFactory(
        objetivo=ObjetivosCampanhaEnum.cadastro,
        criado_por=superior.fk_membro_id,
    )
    database.session.add(campanha_cadastro)
    database.session.commit()

    data = {
        'nome': 'Eric',
        'email': 'teste@email.com',
        'telefone': '85998685421',
        'origem_cadastro': OrigemCadastroEnum.acutis,
        'nome_social': 'Eric Gomes',
        'pais': 'brasil',
        'numero_documento': '888812345678',
        'data_nascimento': '2003-01-21',
        'sexo': SexoEnum.masculino,
        'senha': '#Teste;@123',
        'endereco': json.dumps({
            'codigo_postal': '58053-022',
            'tipo_logradouro': 'Rua',
            'logradouro': 'José Firmino da Silva',
            'numero': '884',
            'complemento': 'Casa',
            'bairro': 'Jardim São Paulo',
            'cidade': 'João Pessoa',
            'estado': 'PB',
            'pais': 'brasil',
        }),
    }

    response = client.post(
        f'/api/admin/campanhas/cadastro-por-campanha/{campanha_cadastro.id}',
        data=data,
        content_type='multipart/form-data',
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json == {'msg': 'Membro cadastrado com sucesso.'}

    membro_cadastrado = (
        database.session.query(Membro)
        .filter(Membro.numero_documento == '888812345678')
        .first()
    )

    assert membro_cadastrado is not None


def test_cadastro_por_campanha_lead(client: FlaskClient, seed_membros_oficial):
    superior = seed_membros_oficial[0]

    campanha_lead = CampanhaFactory(
        objetivo=ObjetivosCampanhaEnum.pre_cadastro,
        criado_por=superior.fk_membro_id,
    )
    database.session.add(campanha_lead)
    database.session.commit()

    data = {
        'nome': 'Eric',
        'email': 'teste@email.com',
        'telefone': '85998685421',
        'origem_cadastro': OrigemCadastroEnum.acutis,
        'pais': 'brasil',
        'senha': '#Teste;@123',
    }

    response = client.post(
        f'/api/admin/campanhas/cadastro-por-campanha/{campanha_lead.id}',
        data=data,
        content_type='multipart/form-data',
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json == {'msg': 'Lead cadastrado com sucesso.'}

    lead_cadastrado = (
        database.session.query(Lead)
        .filter(Lead.email == 'teste@email.com')
        .first()
    )

    assert lead_cadastrado is not None


def test_cadastro_por_campanha_email_ja_cadastrado(
    client: FlaskClient, seed_registrar_membro, seed_membros_oficial
):
    lead, _, _ = seed_registrar_membro(status=True)

    superior = seed_membros_oficial[0]

    campanha_lead = CampanhaFactory(
        objetivo=ObjetivosCampanhaEnum.pre_cadastro,
        criado_por=superior.fk_membro_id,
    )

    database.session.add(campanha_lead)
    database.session.commit()

    data = {
        'nome': 'Eric',
        'email': lead.email,
        'telefone': '85998685421',
        'origem_cadastro': lead.origem_cadastro,
        'pais': lead.pais,
        'senha': '#Teste;@123',
    }
    response = client.post(
        f'/api/admin/campanhas/cadastro-por-campanha/{campanha_lead.id}',
        data=data,
        content_type='multipart/form-data',
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json == [{'msg': 'O e-mail informado já está cadastro.'}]


def test_cadastro_por_campanha_telefone_ja_cadastrado(
    client: FlaskClient, seed_registrar_membro, seed_membros_oficial
):
    lead, _, _ = seed_registrar_membro(
        nome='Eric', status=True, telefone='85998685421'
    )

    superior = seed_membros_oficial[0]

    campanha_lead = CampanhaFactory(
        objetivo=ObjetivosCampanhaEnum.pre_cadastro,
        criado_por=superior.fk_membro_id,
    )

    database.session.add(campanha_lead)
    database.session.commit()

    data = {
        'nome': 'Eric',
        'email': 'teste@email.com',
        'telefone': lead.telefone,
        'origem_cadastro': lead.origem_cadastro,
        'pais': lead.pais,
        'senha': '#Teste;@123',
    }
    response = client.post(
        f'/api/admin/campanhas/cadastro-por-campanha/{campanha_lead.id}',
        data=data,
        content_type='multipart/form-data',
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json == [{'msg': 'O telefone informado já tem cadastro.'}]


def test_cadastro_por_campanha_superior_obrigatorio(
    client: FlaskClient,
    seed_membros_oficial,
):
    superior = seed_membros_oficial[0]

    cargo_oficial = CargosOficiaisFactory(criado_por=superior.fk_membro_id)

    database.session.add(cargo_oficial)
    database.session.commit()

    campanha_oficiais = CampanhaMembroOficialFactory(
        criado_por=superior.fk_membro_id,
        fk_cargo_oficial_id=cargo_oficial.id,
        superior_obrigatorio=True,
    )
    database.session.add(campanha_oficiais)
    database.session.commit()

    tipos_campos_adicionais = [
        {'tipo_campo': 'date', 'obrigatorio': True},
        {'tipo_campo': 'arquivo', 'obrigatorio': False},
    ]

    campos_adicionais = []
    for campo in tipos_campos_adicionais:
        campo_adicional = CampoAdicionalFactory(
            fk_campanha_id=campanha_oficiais.id,
            tipo_campo=campo['tipo_campo'],
            obrigatorio=campo['obrigatorio'],
        )
        campos_adicionais.append(campo_adicional)
    database.session.add_all(campos_adicionais)
    database.session.commit()

    data = {
        'nome': 'Eric',
        'email': 'teste@email.com',
        'telefone': '85998685421',
        'origem_cadastro': OrigemCadastroEnum.acutis,
        'nome_social': 'Eric Gomes',
        'pais': 'brasil',
    }

    response = client.post(
        f'/api/admin/campanhas/cadastro-por-campanha/{campanha_oficiais.id}',
        data=data,
        content_type='multipart/form-data',
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json == [{'msg': 'É necessário informar o superior.'}]


def test_cadastro_por_campanha_json_invalido(
    client: FlaskClient,
    seed_registrar_membro,
    seed_membros_oficial,
):
    lead, membro, endereco = seed_registrar_membro(status=True)

    superior = seed_membros_oficial[0]

    token = client.post(
        '/api/autenticacao/login?httponly=false',
        json={
            'email': lead.email,
            'senha': '#Teste;@123',
        },
    ).get_json()['access_token']

    campanha_cadastro = CampanhaFactory(
        objetivo=ObjetivosCampanhaEnum.cadastro,
        criado_por=superior.fk_membro_id,
    )
    database.session.add(campanha_cadastro)
    database.session.commit()

    data = {
        'nome': 'Eric',
        'email': lead.email,
        'telefone': lead.telefone,
        'origem_cadastro': lead.origem_cadastro,
        'nome_social': 'Eric Gomes',
        'numero_documento': membro.numero_documento,
        'data_nascimento': membro.data_nascimento.strftime('%Y-%m-%d'),
        'sexo': membro.sexo,
        'superior': str(superior.fk_membro_id),
        'endereco': {
            'codigo_postal': endereco.codigo_postal,
            'tipo_logradouro': endereco.tipo_logradouro,
            'logradouro': endereco.logradouro,
            'numero': endereco.numero,
            'complemento': endereco.complemento,
            'bairro': endereco.bairro,
            'cidade': endereco.cidade,
            'estado': endereco.estado,
            'pais': endereco.pais,
        },
    }

    response = client.post(
        f'/api/admin/campanhas/cadastro-por-campanha/{campanha_cadastro.id}',
        headers={'Authorization': f'Bearer {token}'},
        data=data,
        content_type='multipart/form-data',
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert (
        response.json[0]['msg']
        == 'Value error, O campo "endereco" deve ser um JSON válido.'
    )


def test_cadastro_por_campanha_documento_invalido(
    client: FlaskClient,
    seed_registrar_membro,
    seed_membros_oficial,
):
    lead, membro, endereco = seed_registrar_membro(status=True)

    superior = seed_membros_oficial[0]

    campanha_cadastro = CampanhaFactory(
        objetivo=ObjetivosCampanhaEnum.cadastro,
        criado_por=superior.fk_membro_id,
    )
    database.session.add(campanha_cadastro)
    database.session.commit()

    data = {
        'nome': 'Eric',
        'email': lead.email,
        'telefone': lead.telefone,
        'origem_cadastro': lead.origem_cadastro,
        'nome_social': 'Eric Gomes',
        'numero_documento': '121',
        'data_nascimento': membro.data_nascimento.strftime('%Y-%m-%d'),
        'sexo': membro.sexo,
        'endereco': json.dumps({
            'codigo_postal': endereco.codigo_postal,
            'tipo_logradouro': endereco.tipo_logradouro,
            'logradouro': endereco.logradouro,
            'numero': endereco.numero,
            'complemento': endereco.complemento,
            'bairro': endereco.bairro,
            'cidade': endereco.cidade,
            'estado': endereco.estado,
            'pais': endereco.pais,
        }),
    }

    response = client.post(
        f'/api/admin/campanhas/cadastro-por-campanha/{campanha_cadastro.id}',
        data=data,
        content_type='multipart/form-data',
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert (
        response.json[0]['msg']
        == 'O documento deve conter entre 11 e 50 caracteres.'
    )


def test_cadastro_por_campanha_nome_social_invalido(
    client: FlaskClient,
    seed_registrar_membro,
    seed_membros_oficial,
):
    lead, membro, endereco = seed_registrar_membro(status=True)

    superior = seed_membros_oficial[0]

    campanha_cadastro = CampanhaFactory(
        objetivo=ObjetivosCampanhaEnum.cadastro,
        criado_por=superior.fk_membro_id,
    )
    database.session.add(campanha_cadastro)
    database.session.commit()

    data = {
        'nome': 'Eric',
        'email': lead.email,
        'telefone': lead.telefone,
        'origem_cadastro': lead.origem_cadastro,
        'nome_social': 'Joao Z3z1m',
        'numero_documento': membro.numero_documento,
        'data_nascimento': membro.data_nascimento.strftime('%Y-%m-%d'),
        'sexo': membro.sexo,
        'endereco': json.dumps({
            'codigo_postal': endereco.codigo_postal,
            'tipo_logradouro': endereco.tipo_logradouro,
            'logradouro': endereco.logradouro,
            'numero': endereco.numero,
            'complemento': endereco.complemento,
            'bairro': endereco.bairro,
            'cidade': endereco.cidade,
            'estado': endereco.estado,
            'pais': endereco.pais,
        }),
    }

    response = client.post(
        f'/api/admin/campanhas/cadastro-por-campanha/{campanha_cadastro.id}',
        data=data,
        content_type='multipart/form-data',
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert (
        response.json[0]['msg']
        == 'O nome social Joao Z3z1m possui caracteres inválidos.'
    )


def test_cadastro_por_campanha_nome_invalido(
    client: FlaskClient,
    seed_registrar_membro,
    seed_membros_oficial,
):
    lead, membro, endereco = seed_registrar_membro(status=True)

    superior = seed_membros_oficial[0]

    campanha_cadastro = CampanhaFactory(
        objetivo=ObjetivosCampanhaEnum.cadastro,
        criado_por=superior.fk_membro_id,
    )
    database.session.add(campanha_cadastro)
    database.session.commit()

    data = {
        'nome': 'Joao Z3z1m',
        'email': lead.email,
        'telefone': lead.telefone,
        'origem_cadastro': lead.origem_cadastro,
        'nome_social': 'Eric Gomes',
        'numero_documento': membro.numero_documento,
        'data_nascimento': membro.data_nascimento.strftime('%Y-%m-%d'),
        'sexo': membro.sexo,
        'endereco': json.dumps({
            'codigo_postal': endereco.codigo_postal,
            'tipo_logradouro': endereco.tipo_logradouro,
            'logradouro': endereco.logradouro,
            'numero': endereco.numero,
            'complemento': endereco.complemento,
            'bairro': endereco.bairro,
            'cidade': endereco.cidade,
            'estado': endereco.estado,
            'pais': endereco.pais,
        }),
    }

    response = client.post(
        f'/api/admin/campanhas/cadastro-por-campanha/{campanha_cadastro.id}',
        data=data,
        content_type='multipart/form-data',
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert (
        response.json[0]['msg']
        == 'O nome Joao Z3z1m possui caracteres inválidos.'
    )


def test_cadastro_por_campanha_nome_curto(
    client: FlaskClient,
    seed_registrar_membro,
    seed_membros_oficial,
):
    lead, membro, endereco = seed_registrar_membro(status=True)

    superior = seed_membros_oficial[0]

    campanha_cadastro = CampanhaFactory(
        objetivo=ObjetivosCampanhaEnum.cadastro,
        criado_por=superior.fk_membro_id,
    )
    database.session.add(campanha_cadastro)
    database.session.commit()

    data = {
        'nome': 'E',
        'email': lead.email,
        'telefone': lead.telefone,
        'origem_cadastro': lead.origem_cadastro,
        'nome_social': 'Eric Gomes',
        'numero_documento': membro.numero_documento,
        'data_nascimento': membro.data_nascimento.strftime('%Y-%m-%d'),
        'sexo': membro.sexo,
        'endereco': json.dumps({
            'codigo_postal': endereco.codigo_postal,
            'tipo_logradouro': endereco.tipo_logradouro,
            'logradouro': endereco.logradouro,
            'numero': endereco.numero,
            'complemento': endereco.complemento,
            'bairro': endereco.bairro,
            'cidade': endereco.cidade,
            'estado': endereco.estado,
            'pais': endereco.pais,
        }),
    }

    response = client.post(
        f'/api/admin/campanhas/cadastro-por-campanha/{campanha_cadastro.id}',
        data=data,
        content_type='multipart/form-data',
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert (
        response.json[0]['msg']
        == 'O nome deve conter entre 3 e 100 caracteres.'
    )
