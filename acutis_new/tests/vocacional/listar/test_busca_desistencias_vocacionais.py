from datetime import datetime
from http import HTTPStatus

from flask.testing import FlaskClient

from acutis_api.domain.entities.etapa_vocacional import (
    EtapaVocacional,
    PassosVocacionalEnum,
    PassosVocacionalStatusEnum,
)
from acutis_api.domain.entities.usuario_vocacional import UsuarioVocacional
from acutis_api.infrastructure.extensions import database
from tests.factories import UsuarioVocacionalFactory


def test_busca_desistencias_vocacionais(
    client: FlaskClient,
    membro_token,
    seed_pre_cadastro_vocacional_desistencia,
):
    seed_pre_cadastro_vocacional_desistencia()
    total_registros = 1

    response = client.get(
        '/api/vocacional/listar-desistencias-vocacionais',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    data_response = response.get_json()

    assert data_response['total'] == total_registros


def test_busca_desistencias_por_brasil(
    client: FlaskClient,
    membro_token,
    seed_pre_cadastro_vocacional_desistencia,
):
    seed_pre_cadastro_vocacional_desistencia(pais='brasil')
    total_registros = 1

    response = client.get(
        '/api/vocacional/listar-desistencias-vocacionais?pais=brasil',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    data_response = response.get_json()
    assert data_response['total'] == total_registros
    desistencia = data_response['desistencias'][0]
    assert desistencia['pais'] == 'brasil'


def test_busca_desistencias_por_outros_paises(
    client: FlaskClient,
    membro_token,
    seed_pre_cadastro_vocacional_desistencia,
):
    seed_pre_cadastro_vocacional_desistencia(pais='brasil')
    seed_pre_cadastro_vocacional_desistencia(pais='argentina')
    total_registros = 1

    response = client.get(
        '/api/vocacional/listar-desistencias-vocacionais?pais=argentina',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    data_response = response.get_json()
    assert data_response['total'] == total_registros
    desistencia = data_response['desistencias'][0]
    assert desistencia['pais'] != 'brasil'


def test_busca_desistencias_vocacionais_por_telefone(
    client: FlaskClient,
    membro_token,
    seed_pre_cadastro_vocacional_desistencia,
):
    total_registros = 1

    seed_pre_cadastro_vocacional_desistencia(telefone='11999999999')
    seed_pre_cadastro_vocacional_desistencia(telefone='11988888888')

    response = client.get(
        '/api/vocacional/listar-desistencias-vocacionais?telefone=11999999999',
        headers={'Authorization': f'Bearer {membro_token}'},
    )
    assert response.status_code == HTTPStatus.OK
    data_response = response.get_json()
    assert data_response['total'] == total_registros
    desistencia = data_response['desistencias'][0]
    assert desistencia['telefone'] == '11999999999'


def test_busca_desistencias_vocacionais_por_nome(
    client: FlaskClient,
    membro_token,
    seed_pre_cadastro_vocacional_desistencia,
):
    total_registros = 1

    seed_pre_cadastro_vocacional_desistencia(nome='joao')
    seed_pre_cadastro_vocacional_desistencia(nome='maria')

    response = client.get(
        '/api/vocacional/listar-desistencias-vocacionais?nome=maria',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    data_response = response.get_json()
    assert data_response['total'] == total_registros
    desistencia = data_response['desistencias'][0]
    assert desistencia['nome'] == 'maria'


def test_busca_desistencias_vocacionais_por_email(
    client: FlaskClient,
    membro_token,
    seed_pre_cadastro_vocacional_desistencia,
):
    total_registros = 1

    seed_pre_cadastro_vocacional_desistencia(email='teste@gmail.com')
    seed_pre_cadastro_vocacional_desistencia(email='maria@gmail.com')

    response = client.get(
        '/api/vocacional/listar-desistencias-vocacionais?email=teste@gmail.com',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    data_response = response.get_json()
    assert data_response['total'] == total_registros
    desistencia = data_response['desistencias'][0]
    assert desistencia['email'] == 'teste@gmail.com'


def test_busca_desistencias_vocacionais_por_data_inicial(
    client: FlaskClient,
    membro_token,
    seed_pre_cadastro_vocacional_desistencia,
    mock_db_time,
):
    total_registros = 1

    seed_pre_cadastro_vocacional_desistencia()

    with mock_db_time(model=UsuarioVocacional, time=datetime(2035, 3, 10)):
        pre_cadastro_2 = UsuarioVocacionalFactory(nome='João')

        database.session.add(pre_cadastro_2)
        database.session.flush()

    with mock_db_time(model=EtapaVocacional, time=datetime(2035, 3, 10)):
        new_etapa = EtapaVocacional(
            fk_usuario_vocacional_id=pre_cadastro_2.id,
            etapa=PassosVocacionalEnum.pre_cadastro,
            status=PassosVocacionalStatusEnum.desistencia,
            justificativa=None,
            fk_responsavel_id=None,
        )

        database.session.add(new_etapa)
        database.session.commit()

    response = client.get(
        '/api/vocacional/listar-desistencias-vocacionais?data_inicial=2035-03-10',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    data_response = response.get_json()
    assert data_response['total'] == total_registros
    desistencia = data_response['desistencias'][0]
    assert desistencia['nome'] == 'João'


def test_busca_desistencias_vocacionais_por_data_final(
    client: FlaskClient,
    membro_token,
    seed_pre_cadastro_vocacional_desistencia,
    mock_db_time,
):
    total_registros = 1

    seed_pre_cadastro_vocacional_desistencia()

    with mock_db_time(model=UsuarioVocacional, time=datetime(2023, 3, 10)):
        pre_cadastro_2 = UsuarioVocacionalFactory(nome='João')

        database.session.add(pre_cadastro_2)
        database.session.flush()

    with mock_db_time(model=EtapaVocacional, time=datetime(2023, 3, 10)):
        new_etapa = EtapaVocacional(
            fk_usuario_vocacional_id=pre_cadastro_2.id,
            etapa=PassosVocacionalEnum.pre_cadastro,
            status=PassosVocacionalStatusEnum.desistencia,
            justificativa=None,
            fk_responsavel_id=None,
        )

        database.session.add(new_etapa)
        database.session.commit()

    response = client.get(
        '/api/vocacional/listar-desistencias-vocacionais?data_final=2024-03-10',
        headers={'Authorization': f'Bearer {membro_token}'},
    )
    assert response.status_code == HTTPStatus.OK
    data_response = response.get_json()
    assert data_response['total'] == total_registros
    desistencia = data_response['desistencias'][0]
    assert desistencia['nome'] == 'João'


def test_busca_desistencias_vocacionais_por_genero(
    client: FlaskClient,
    membro_token,
    seed_pre_cadastro_vocacional_desistencia,
):
    total_registros = 1

    seed_pre_cadastro_vocacional_desistencia(genero='masculino')
    seed_pre_cadastro_vocacional_desistencia(genero='feminino')

    response = client.get(
        '/api/vocacional/listar-desistencias-vocacionais?genero=feminino',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    data_response = response.get_json()
    assert data_response['total'] == total_registros
    desistencia = data_response['desistencias'][0]
    assert desistencia['genero'] == 'feminino'


def test_busca_desistencias_vocacionais_por_etapa(
    client: FlaskClient,
    membro_token,
    seed_pre_cadastro_vocacional_desistencia,
):
    total_registros = 1

    seed_pre_cadastro_vocacional_desistencia(
        etapa=PassosVocacionalEnum.pre_cadastro
    )
    seed_pre_cadastro_vocacional_desistencia(
        etapa=PassosVocacionalEnum.cadastro
    )

    response = client.get(
        '/api/vocacional/listar-desistencias-vocacionais?etapa=cadastro',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    data_response = response.get_json()
    assert data_response['total'] == total_registros
    desistencia = data_response['desistencias'][0]
    assert desistencia['etapa'] == PassosVocacionalEnum.cadastro
