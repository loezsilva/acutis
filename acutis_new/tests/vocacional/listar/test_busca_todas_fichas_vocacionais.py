from datetime import datetime
from http import HTTPStatus

from faker import Faker
from flask.testing import FlaskClient

from acutis_api.communication.enums.vocacional import (
    PassosVocacionalStatusEnum,
)
from acutis_api.domain.entities.etapa_vocacional import EtapaVocacional
from acutis_api.domain.entities.ficha_vocacional import FichaVocacional
from acutis_api.domain.entities.usuario_vocacional import GeneroVocacionalEnum
from acutis_api.infrastructure.extensions import database
from tests.factories import (
    FichaVocacionalFactory,
)

faker = Faker('pt_BR')


def test_busca_ficha_vocacional(
    client: FlaskClient, membro_token, seed_ficha_vocacional
):
    response = client.get(
        '/api/vocacional/listar-fichas-vocacionais',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK

    data_response = response.get_json()

    assert 'fichas_vocacionais' in data_response
    assert 'pagina' in data_response
    assert 'total' in data_response


def test_busca_ficha_vocacional_por_brasil(
    client: FlaskClient, membro_token, seed_ficha_vocacional
):
    total_registros = 1

    seed_ficha_vocacional(pais='brasil')

    seed_ficha_vocacional(pais='argentina')

    response = client.get(
        '/api/vocacional/listar-fichas-vocacionais?pais=brasil',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK

    data_response = response.get_json()
    ficha = response.json['fichas_vocacionais'][0]['pre_cadastro']
    assert ficha['pais'] == 'brasil'
    assert data_response['total'] == total_registros


def test_busca_ficha_vocacional_por_outros_paises(
    client: FlaskClient, membro_token, seed_ficha_vocacional
):
    total_registros = 1

    seed_ficha_vocacional(pais='brasil')

    seed_ficha_vocacional(pais='argentina')

    response = client.get(
        '/api/vocacional/listar-fichas-vocacionais?pais=argetina',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK

    data_response = response.get_json()
    ficha = response.json['fichas_vocacionais'][0]['pre_cadastro']
    assert ficha['pais'] != 'brasil'
    assert data_response['total'] == total_registros


def test_busca_ficha_vocacional_por_telefone(
    client: FlaskClient, membro_token, seed_ficha_vocacional
):
    total_registros = 1

    seed_ficha_vocacional(telefone='83998422828')

    seed_ficha_vocacional(telefone='83998422829')

    response = client.get(
        '/api/vocacional/listar-fichas-vocacionais?telefone=83998422828',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK

    data_response = response.get_json()
    ficha = response.json['fichas_vocacionais'][0]['pre_cadastro']
    assert ficha['telefone'] == '83998422828'
    assert data_response['total'] == total_registros


def test_busca_ficha_vocacional_por_status(
    client: FlaskClient, membro_token, seed_ficha_vocacional
):
    total_registros = 1

    seed_ficha_vocacional(status=PassosVocacionalStatusEnum.aprovado)

    seed_ficha_vocacional(status=PassosVocacionalStatusEnum.reprovado)

    response = client.get(
        '/api/vocacional/listar-fichas-vocacionais?status=aprovado',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK

    data_response = response.get_json()
    ficha = response.json['fichas_vocacionais'][0]['pre_cadastro']
    assert ficha['status'] == PassosVocacionalStatusEnum.aprovado
    assert data_response['total'] == total_registros


def test_busca_ficha_vocacional_por_nome(
    client: FlaskClient, membro_token, seed_ficha_vocacional
):
    total_registros = 1

    seed_ficha_vocacional(nome='joao')

    seed_ficha_vocacional(nome='maria')

    response = client.get(
        '/api/vocacional/listar-fichas-vocacionais?nome=joao',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK

    data_response = response.get_json()
    ficha = response.json['fichas_vocacionais'][0]['pre_cadastro']
    assert ficha['nome'] == 'joao'
    assert data_response['total'] == total_registros


def test_busca_ficha_vocacional_email(
    client: FlaskClient, membro_token, seed_ficha_vocacional
):
    total_registros = 1

    seed_ficha_vocacional(email='teste@gmail.com')

    seed_ficha_vocacional(email='maria@gmail.com')

    response = client.get(
        '/api/vocacional/listar-fichas-vocacionais?email=teste@gmail.com',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK

    data_response = response.get_json()
    ficha = response.json['fichas_vocacionais'][0]['pre_cadastro']
    assert ficha['email'] == 'teste@gmail.com'
    assert data_response['total'] == total_registros


def test_busca_ficha_vocacional_por_data_inicial(
    client: FlaskClient,
    membro_token,
    seed_ficha_vocacional,
    seed_cadastro_vocacional_aprovado,
    mock_db_time,
):
    total_registros = 1

    seed_ficha_vocacional()

    pre_cadastro, _ = seed_cadastro_vocacional_aprovado(
        nome='João',
    )

    with mock_db_time(model=FichaVocacional, time=datetime(2035, 3, 10)):
        ficha_2 = FichaVocacionalFactory(
            fk_usuario_vocacional_id=pre_cadastro.id,
        )
        database.session.add(ficha_2)
        database.session.commit()

    with mock_db_time(model=EtapaVocacional, time=datetime(2035, 3, 10)):
        new_etapa_ficha_vocacional = EtapaVocacional(
            fk_usuario_vocacional_id=pre_cadastro.id,
            etapa='ficha_vocacional',
            status='pendente',
            justificativa=None,
            fk_responsavel_id=None,
        )

        database.session.add(new_etapa_ficha_vocacional)
        database.session.commit()

    response = client.get(
        '/api/vocacional/listar-fichas-vocacionais?data_inicial=2035-03-10',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK

    data_response = response.get_json()
    ficha = response.json['fichas_vocacionais'][0]['pre_cadastro']
    assert ficha['nome'] == 'João'
    assert data_response['total'] == total_registros


def test_busca_ficha_vocacional_por_data_final(
    client: FlaskClient,
    membro_token,
    seed_ficha_vocacional,
    seed_cadastro_vocacional_aprovado,
    mock_db_time,
):
    total_registros = 1

    seed_ficha_vocacional()

    pre_cadastro, _ = seed_cadastro_vocacional_aprovado(
        nome='João',
    )

    with mock_db_time(model=FichaVocacional, time=datetime(2023, 3, 10)):
        ficha_2 = FichaVocacionalFactory(
            fk_usuario_vocacional_id=pre_cadastro.id,
        )
        database.session.add(ficha_2)
        database.session.commit()

    with mock_db_time(model=EtapaVocacional, time=datetime(2035, 3, 10)):
        new_etapa_ficha_vocacional = EtapaVocacional(
            fk_usuario_vocacional_id=pre_cadastro.id,
            etapa='ficha_vocacional',
            status='pendente',
            justificativa=None,
            fk_responsavel_id=None,
        )

        database.session.add(new_etapa_ficha_vocacional)
        database.session.commit()

    response = client.get(
        '/api/vocacional/listar-fichas-vocacionais?data_final=2024-03-10',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK

    data_response = response.get_json()
    ficha = response.json['fichas_vocacionais'][0]['pre_cadastro']
    assert ficha['nome'] == 'João'
    assert data_response['total'] == total_registros


def test_busca_ficha_vocacional_documento(
    client: FlaskClient, membro_token, seed_ficha_vocacional
):
    total_registros = 1

    seed_ficha_vocacional(documento_identidade='123456789')

    seed_ficha_vocacional()

    response = client.get(
        '/api/vocacional/listar-fichas-vocacionais?documento_identidade=123456789',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK

    data_response = response.get_json()
    ficha = response.json['fichas_vocacionais'][0]['cadastro_vocacional']
    assert ficha['documento_identidade'] == '123456789'
    assert data_response['total'] == total_registros


def test_busca_ficha_vocacional_por_usuario_vocacional_id(
    client: FlaskClient, membro_token, seed_ficha_vocacional
):
    total_registros = 1

    pre_cadastro, _, _ = seed_ficha_vocacional(nome='João')

    seed_ficha_vocacional(genero=GeneroVocacionalEnum.feminino)

    response = client.get(
        f'/api/vocacional/listar-fichas-vocacionais?fk_usuario_vocacional_id={pre_cadastro.id}',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK

    data_response = response.get_json()
    ficha = response.json['fichas_vocacionais'][0]['pre_cadastro']
    assert ficha['nome'] == 'João'
    assert data_response['total'] == total_registros


def test_busca_ficha_vocacional_por_genero(
    client: FlaskClient, membro_token, seed_ficha_vocacional
):
    total_registros = 1

    seed_ficha_vocacional(genero=GeneroVocacionalEnum.masculino)

    seed_ficha_vocacional(genero=GeneroVocacionalEnum.feminino)

    response = client.get(
        '/api/vocacional/listar-fichas-vocacionais?genero=masculino',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK

    data_response = response.get_json()
    ficha = response.json['fichas_vocacionais'][0]['pre_cadastro']
    assert ficha['genero'] == GeneroVocacionalEnum.masculino
    assert data_response['total'] == total_registros
