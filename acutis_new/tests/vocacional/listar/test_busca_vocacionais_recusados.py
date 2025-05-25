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


def test_busca_vocacionais_recusados(
    client: FlaskClient, membro_token, seed_vocacionais_reprovados
):
    total_registros = 5

    response = client.get(
        '/api/vocacional/listar-vocacionais-recusados',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    data_response = response.get_json()
    assert data_response['total'] == total_registros
    assert data_response['recusados'][0]['responsavel'] is not None


def test_busca_vocacionais_recusados_por_brasil(
    client: FlaskClient, membro_token, seed_vocacional_reprovado
):
    seed_vocacional_reprovado(pais='brasil')
    seed_vocacional_reprovado(pais='argentina')

    total_registros = 1

    response = client.get(
        '/api/vocacional/listar-vocacionais-recusados?pais=brasil',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    data_response = response.get_json()
    assert data_response['total'] == total_registros
    recusado = data_response['recusados'][0]
    assert recusado['pais'] == 'brasil'


def test_busca_vocacionais_recusados_por_outros_paises(
    client: FlaskClient,
    membro_token,
    seed_vocacional_reprovado,
):
    seed_vocacional_reprovado(pais='brasil')
    seed_vocacional_reprovado(pais='argentina')
    total_registros = 1

    response = client.get(
        '/api/vocacional/listar-vocacionais-recusados?pais=argentina',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    data_response = response.get_json()
    assert data_response['total'] == total_registros
    recusado = data_response['recusados'][0]
    assert recusado['pais'] != 'brasil'


def test_busca_vocacionais_recusados_por_telefone(
    client: FlaskClient,
    membro_token,
    seed_vocacional_reprovado,
):
    total_registros = 1

    seed_vocacional_reprovado(telefone='11999999999')
    seed_vocacional_reprovado(telefone='11988888888')

    response = client.get(
        '/api/vocacional/listar-vocacionais-recusados?telefone=11999999999',
        headers={'Authorization': f'Bearer {membro_token}'},
    )
    assert response.status_code == HTTPStatus.OK
    data_response = response.get_json()
    assert data_response['total'] == total_registros
    recusado = data_response['recusados'][0]
    assert recusado['telefone'] == '11999999999'


def test_busca_vocacionais_recusados_por_nome(
    client: FlaskClient,
    membro_token,
    seed_vocacional_reprovado,
):
    total_registros = 1

    seed_vocacional_reprovado(nome='joao')
    seed_vocacional_reprovado(nome='maria')

    response = client.get(
        '/api/vocacional/listar-vocacionais-recusados?nome=maria',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    data_response = response.get_json()
    assert data_response['total'] == total_registros
    recusado = data_response['recusados'][0]
    assert recusado['nome'] == 'maria'


def test_busca_vocacionais_recusados_por_email(
    client: FlaskClient,
    membro_token,
    seed_vocacional_reprovado,
):
    total_registros = 1

    seed_vocacional_reprovado(email='teste@gmail.com')
    seed_vocacional_reprovado(email='maria@gmail.com')

    response = client.get(
        '/api/vocacional/listar-vocacionais-recusados?email=teste@gmail.com',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    data_response = response.get_json()
    assert data_response['total'] == total_registros
    recusado = data_response['recusados'][0]
    assert recusado['email'] == 'teste@gmail.com'


def test_busca_vocacionais_recusados_por_data_inicial(
    client: FlaskClient, membro_token, seed_vocacional_reprovado, mock_db_time
):
    total_registros = 1

    seed_vocacional_reprovado()

    with mock_db_time(model=UsuarioVocacional, time=datetime(2035, 3, 11)):
        new_pre_cadastro = UsuarioVocacionalFactory(nome='João')

        database.session.add(new_pre_cadastro)
        database.session.flush()

    with mock_db_time(model=EtapaVocacional, time=datetime(2035, 3, 11)):
        new_etapa = EtapaVocacional(
            fk_usuario_vocacional_id=new_pre_cadastro.id,
            etapa=PassosVocacionalEnum.pre_cadastro,
            status=PassosVocacionalStatusEnum.reprovado,
            justificativa=None,
            fk_responsavel_id=None,
        )

        database.session.add(new_etapa)
        database.session.commit()

    response = client.get(
        '/api/vocacional/listar-vocacionais-recusados?data_inicial=2035-03-10',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    data_response = response.get_json()
    assert data_response['total'] == total_registros
    recusado = data_response['recusados'][0]
    assert recusado['nome'] == 'João'


def test_busca_vocacionais_recusados_por_data_final(
    client: FlaskClient, membro_token, seed_vocacional_reprovado, mock_db_time
):
    total_registros = 1

    seed_vocacional_reprovado()

    with mock_db_time(model=UsuarioVocacional, time=datetime(2023, 3, 11)):
        new_pre_cadastro = UsuarioVocacionalFactory(nome='João')

        database.session.add(new_pre_cadastro)
        database.session.flush()

    with mock_db_time(model=EtapaVocacional, time=datetime(2023, 3, 11)):
        new_etapa = EtapaVocacional(
            fk_usuario_vocacional_id=new_pre_cadastro.id,
            etapa=PassosVocacionalEnum.pre_cadastro,
            status=PassosVocacionalStatusEnum.reprovado,
            justificativa=None,
            fk_responsavel_id=None,
        )

        database.session.add(new_etapa)
        database.session.commit()

    response = client.get(
        '/api/vocacional/listar-vocacionais-recusados?data_final=2024-03-10',
        headers={'Authorization': f'Bearer {membro_token}'},
    )
    assert response.status_code == HTTPStatus.OK
    data_response = response.get_json()
    assert data_response['total'] == total_registros
    recusado = data_response['recusados'][0]
    assert recusado['nome'] == 'João'


def test_busca_vocacionais_recusados_por_genero(
    client: FlaskClient,
    membro_token,
    seed_vocacional_reprovado,
):
    total_registros = 1

    seed_vocacional_reprovado(genero='feminino')
    seed_vocacional_reprovado(genero='masculino')

    response = client.get(
        '/api/vocacional/listar-vocacionais-recusados?genero=feminino',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    data_response = response.get_json()
    assert data_response['total'] == total_registros
    recusado = data_response['recusados'][0]
    assert recusado['genero'] == 'feminino'


def test_busca_recusados_por_etapa(
    client: FlaskClient,
    membro_token,
    seed_vocacional_reprovado,
):
    total_registros = 1

    seed_vocacional_reprovado(etapa=PassosVocacionalEnum.pre_cadastro)
    seed_vocacional_reprovado(etapa=PassosVocacionalEnum.cadastro)

    response = client.get(
        '/api/vocacional/listar-vocacionais-recusados?etapa=pre_cadastro',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    data_response = response.get_json()
    assert data_response['total'] == total_registros
    recusado = data_response['recusados'][0]
    assert recusado['etapa'] == PassosVocacionalEnum.pre_cadastro
