from datetime import datetime
from http import HTTPStatus

from flask.testing import FlaskClient

from acutis_api.domain.entities.lead import Lead
from acutis_api.domain.entities.membro import Membro
from acutis_api.infrastructure.extensions import database
from tests.factories import (
    CampanhaFactory,
    EnderecoFactory,
    LeadCampanhaFactory,
    LeadFactory,
    MembroFactory,
)

SENHA_TESTE = '#Senha@123'


def test_listar_leads_e_membros_sucesso(client: FlaskClient, membro_token):
    total_registros = 2

    lead = LeadFactory()
    lead.senha = SENHA_TESTE
    database.session.add(lead)
    database.session.commit()

    response = client.get(
        '/api/admin/membros/listar-leads-e-membros',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json['total'] == total_registros


def test_listar_leads_e_membros_filtro_ordenar_ascendente(
    client: FlaskClient, membro_token
):
    total_registros = 2

    lead = LeadFactory(nome='aaaaaaaa')
    lead.senha = SENHA_TESTE
    database.session.add(lead)
    database.session.commit()

    response = client.get(
        '/api/admin/membros/listar-leads-e-membros?ordenar_por=nome&tipo_ordenacao=asc',  # noqa
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json['total'] == total_registros
    assert response.json['leads_e_membros'][0]['nome'] == 'aaaaaaaa'


def test_listar_leads_e_membros_filtro_tipo_cadastro_lead(
    client: FlaskClient, membro_token
):
    total_registros = 1

    lead = LeadFactory(nome='Lead Cadastro')
    lead.senha = SENHA_TESTE
    database.session.add(lead)
    database.session.commit()

    response = client.get(
        '/api/admin/membros/listar-leads-e-membros?tipo_cadastro=lead',  # noqa
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json['total'] == total_registros
    assert response.json['leads_e_membros'][0]['nome'] == 'Lead Cadastro'


def test_listar_leads_e_membros_filtro_tipo_cadastro_membro(
    client: FlaskClient, membro_token, seed_registrar_membro
):
    seed_registrar_membro(nome='aaaaaaaa')
    total_registros = 2

    lead = LeadFactory()
    lead.senha = SENHA_TESTE
    database.session.add(lead)
    database.session.commit()

    response = client.get(
        '/api/admin/membros/listar-leads-e-membros?tipo_cadastro=membro&ordenar_por=nome&tipo_ordenacao=asc',  # noqa
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json['total'] == total_registros
    assert response.json['leads_e_membros'][0]['nome'] == 'aaaaaaaa'


def test_listar_leads_e_membros_filtro_nome(
    client: FlaskClient, membro_token, seed_registrar_membro
):
    seed_registrar_membro(nome='Leonardo Neville')
    total_registros = 1

    lead = LeadFactory(nome='Yan da Pororoca')
    lead.senha = SENHA_TESTE
    database.session.add(lead)
    database.session.commit()

    response = client.get(
        '/api/admin/membros/listar-leads-e-membros?nome_email_documento=nevi',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json['total'] == total_registros
    assert response.json['leads_e_membros'][0]['nome'] == 'Leonardo Neville'


def test_listar_leads_e_membros_filtro_numero_documento(
    client: FlaskClient, membro_token, seed_registrar_membro
):
    seed_registrar_membro(numero_documento='48596874125')
    total_registros = 1

    lead = LeadFactory()
    lead.senha = SENHA_TESTE
    database.session.add(lead)
    database.session.commit()

    response = client.get(
        '/api/admin/membros/listar-leads-e-membros?nome_email_documento=4859',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json['total'] == total_registros
    assert (
        response.json['leads_e_membros'][0]['numero_documento']
        == '48596874125'
    )


def test_listar_leads_e_membros_filtro_email(
    client: FlaskClient, membro_token
):
    total_registros = 1

    lead = LeadFactory(email='yantestando123@gmail.com')
    lead.senha = SENHA_TESTE
    database.session.add(lead)
    database.session.commit()

    response = client.get(
        '/api/admin/membros/listar-leads-e-membros?nome_email_documento=yante',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json['total'] == total_registros
    assert (
        response.json['leads_e_membros'][0]['email']
        == 'yantestando123@gmail.com'
    )


def test_listar_leads_e_membros_filtro_telefone(
    client: FlaskClient, membro_token
):
    total_registros = 1

    lead = LeadFactory(telefone='859884868283')
    lead.senha = SENHA_TESTE
    database.session.add(lead)
    database.session.commit()

    response = client.get(
        '/api/admin/membros/listar-leads-e-membros?telefone=86828',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json['total'] == total_registros
    assert response.json['leads_e_membros'][0]['telefone'] == '859884868283'


def test_listar_leads_e_membros_filtro_campanha_id(
    client: FlaskClient, membro_token
):
    total_registros = 1

    lead = LeadFactory(nome='Yan Takabixiga')
    lead.senha = SENHA_TESTE
    database.session.add(lead)

    endereco = EnderecoFactory()
    database.session.add(endereco)

    membro = MembroFactory(fk_lead_id=lead.id, fk_endereco_id=endereco.id)
    database.session.add(membro)

    campanha = CampanhaFactory(criado_por=membro.id)
    database.session.add(campanha)
    database.session.flush()

    lead_campanha = LeadCampanhaFactory(
        fk_lead_id=lead.id,
        fk_campanha_id=campanha.id,
    )
    database.session.add(lead_campanha)

    database.session.commit()

    response = client.get(
        f'/api/admin/membros/listar-leads-e-membros?campanha_origem={
            campanha.id
        }',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json['total'] == total_registros
    assert response.json['leads_e_membros'][0]['nome'] == 'Yan Takabixiga'


def test_listar_leads_e_membros_filtro_data_cadastro_tipo_lead(
    client: FlaskClient,
    membro_token,
    mock_db_time,
):
    total_registros = 1

    lead_1 = LeadFactory()
    lead_1.senha = '#kslfk@123'
    database.session.add(lead_1)
    database.session.commit()

    with mock_db_time(model=Lead, time=datetime(2025, 2, 22)):
        lead_2 = LeadFactory(nome='Yan Takadizordem')
        lead_2.senha = '#kfdsffk@123'
        database.session.add(lead_2)
        database.session.commit()

    response = client.get(
        '/api/admin/membros/listar-leads-e-membros?tipo_cadastro=lead&data_cadastro_inicial=2025-02-21&data_cadastro_final=2025-02-23',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json['total'] == total_registros
    assert response.json['leads_e_membros'][0]['nome'] == 'Yan Takadizordem'


def test_listar_leads_e_membros_filtro_data_cadastro_tipo_membro(
    client: FlaskClient,
    membro_token,
    mock_db_time,
):
    total_registros = 1

    lead = LeadFactory(nome='Yan Miseriqueima')
    lead.senha = '#kslfk@123'
    database.session.add(lead)

    endereco = EnderecoFactory()
    database.session.add(endereco)

    with mock_db_time(model=Membro, time=datetime(2025, 1, 21)):
        membro = MembroFactory(fk_lead_id=lead.id, fk_endereco_id=endereco.id)
        database.session.add(membro)
        database.session.commit()

    response = client.get(
        '/api/admin/membros/listar-leads-e-membros?tipo_cadastro=membro&data_cadastro_inicial=2025-01-21&data_cadastro_final=2025-01-21',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json['total'] == total_registros
    assert response.json['leads_e_membros'][0]['nome'] == 'Yan Miseriqueima'


def test_listar_leads_e_membros_filtro_ultimo_acesso(
    client: FlaskClient,
    membro_token,
    mock_db_time,
):
    total_registros = 1

    with mock_db_time(model=Lead, time=datetime(2025, 1, 15)):
        lead = LeadFactory(nome='Yan KDelas')
        lead.senha = '#qwedf@123'
        database.session.add(lead)
        database.session.commit()

    response = client.get(
        '/api/admin/membros/listar-leads-e-membros?ultimo_acesso_inicial=2025-01-13&ultimo_acesso_final=2025-01-18',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json['total'] == total_registros
    assert response.json['leads_e_membros'][0]['nome'] == 'Yan KDelas'


def test_listar_leads_e_membros_filtro_status_ativo(
    client: FlaskClient,
    membro_token,
):
    total_registros = 2

    lead = LeadFactory(status=True)
    lead.senha = '#qwefdsdf@123'
    database.session.add(lead)
    database.session.commit()

    response = client.get(
        '/api/admin/membros/listar-leads-e-membros?status=true',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json['total'] == total_registros


def test_listar_leads_e_membros_filtro_status_inativo(
    client: FlaskClient,
    membro_token,
):
    total_registros = 1

    lead = LeadFactory(status=False)
    lead.senha = '#qdsf@123'
    database.session.add(lead)
    database.session.commit()

    response = client.get(
        '/api/admin/membros/listar-leads-e-membros?status=false',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json['total'] == total_registros
