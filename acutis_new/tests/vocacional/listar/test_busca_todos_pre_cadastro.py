from datetime import datetime
from http import HTTPStatus

from flask.testing import FlaskClient

from acutis_api.communication.enums.vocacional import (
    PassosVocacionalStatusEnum,
)
from acutis_api.domain.entities.etapa_vocacional import EtapaVocacional
from acutis_api.domain.entities.usuario_vocacional import UsuarioVocacional
from acutis_api.infrastructure.extensions import database
from tests.factories import (
    EtapaVocacionalFactory,
    UsuarioVocacionalFactory,
)


def test_busca_todos_pre_cadastro(
    client: FlaskClient,
    membro_token,
    seed_pre_cadastro_vocacional_pendentes,
):
    response = client.get(
        '/api/vocacional/listar-pre-cadastros',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK


def test_busca_pre_cadastro_por_brasil(client: FlaskClient, membro_token):
    total_registros = 1

    novo_pre_cadastro = UsuarioVocacionalFactory(pais='brasil')
    database.session.add(novo_pre_cadastro)
    database.session.flush()

    etapa = EtapaVocacionalFactory(
        fk_usuario_vocacional_id=novo_pre_cadastro.id,
    )
    database.session.add(etapa)
    database.session.commit()

    response = client.get(
        '/api/vocacional/listar-pre-cadastros?pais=brasil',
        headers={'Authorization': f'Bearer {membro_token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json['total'] == total_registros

    pre_cadastro = response.json['pre_cadastros'][0]['pre_cadastro']
    assert pre_cadastro['pais'] == 'brasil'


def test_busca_pre_cadastro_por_outros_paises(
    client: FlaskClient,
    membro_token,
    seed_pre_cadastro_vocacional_pendentes,
):
    response = client.get(
        '/api/vocacional/listar-pre-cadastros?pais=argentina',
        headers={'Authorization': f'Bearer {membro_token}'},
    )
    assert response.status_code == HTTPStatus.OK

    pre_cadastros = response.json['pre_cadastros']
    for pre_cadastro in pre_cadastros:
        assert pre_cadastro['pre_cadastro']['pais'] != 'brasil'


def test_busca_pre_cadastro_por_telefone(client: FlaskClient, membro_token):
    total_registros = 1

    novo_pre_cadastro = UsuarioVocacionalFactory(telefone='83998422828')
    database.session.add(novo_pre_cadastro)
    database.session.flush()

    etapa = EtapaVocacionalFactory(
        fk_usuario_vocacional_id=novo_pre_cadastro.id,
    )
    database.session.add(etapa)
    database.session.commit()

    response = client.get(
        '/api/vocacional/listar-pre-cadastros?telefone=83998422828',
        headers={'Authorization': f'Bearer {membro_token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json['total'] == total_registros

    pre_cadastro = response.json['pre_cadastros'][0]['pre_cadastro']
    assert pre_cadastro['telefone'] == '83998422828'


def test_busca_pre_cadastro_por_status(client: FlaskClient, membro_token):
    total_registros = 1

    novo_pre_cadastro = UsuarioVocacionalFactory()
    database.session.add(novo_pre_cadastro)
    database.session.flush()

    etapa = EtapaVocacionalFactory(
        fk_usuario_vocacional_id=novo_pre_cadastro.id,
        status=PassosVocacionalStatusEnum.aprovado,
    )
    database.session.add(etapa)
    database.session.commit()

    response = client.get(
        '/api/vocacional/listar-pre-cadastros?status=aprovado',
        headers={'Authorization': f'Bearer {membro_token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json['total'] == total_registros

    pre_cadastro = response.json['pre_cadastros'][0]['pre_cadastro']
    assert pre_cadastro['status'] == PassosVocacionalStatusEnum.aprovado


def test_busca_pre_cadastro_por_nome(client: FlaskClient, membro_token):
    total_registros = 1

    novo_pre_cadastro = UsuarioVocacionalFactory(nome='João')
    database.session.add(novo_pre_cadastro)
    database.session.flush()
    etapa = EtapaVocacionalFactory(
        fk_usuario_vocacional_id=novo_pre_cadastro.id
    )
    database.session.add(etapa)
    database.session.commit()

    pre_cadastro_2 = UsuarioVocacionalFactory(nome='Maria')
    database.session.add(pre_cadastro_2)
    database.session.flush()
    etapa_2 = EtapaVocacionalFactory(
        fk_usuario_vocacional_id=pre_cadastro_2.id
    )
    database.session.add(etapa_2)
    database.session.commit()
    response = client.get(
        '/api/vocacional/listar-pre-cadastros?nome=Maria',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json['total'] == total_registros

    pre_cadastro = response.json['pre_cadastros'][0]['pre_cadastro']
    assert pre_cadastro['nome'] == 'Maria'


def test_busca_pre_cadastro_por_email(client: FlaskClient, membro_token):
    total_registros = 1

    novo_pre_cadastro = UsuarioVocacionalFactory(email='teste@gmail.com')
    database.session.add(novo_pre_cadastro)
    database.session.flush()

    etapa = EtapaVocacionalFactory(
        fk_usuario_vocacional_id=novo_pre_cadastro.id
    )
    database.session.add(etapa)
    database.session.commit()

    response = client.get(
        '/api/vocacional/listar-pre-cadastros?email=teste@gmail.com',
        headers={'Authorization': f'Bearer {membro_token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json['total'] == total_registros

    pre_cadastro = response.json['pre_cadastros'][0]['pre_cadastro']
    assert pre_cadastro['email'] == 'teste@gmail.com'


def test_busca_pre_cadastro_por_data_inicial(
    client: FlaskClient,
    membro_token,
    mock_db_time,
):
    total_registros = 1

    novo_pre_cadastro = UsuarioVocacionalFactory()
    database.session.add(novo_pre_cadastro)
    database.session.flush()

    etapa = EtapaVocacionalFactory(
        fk_usuario_vocacional_id=novo_pre_cadastro.id
    )
    database.session.add(etapa)
    database.session.commit()

    with mock_db_time(model=UsuarioVocacional, time=datetime(2035, 3, 11)):
        pre_cadastro_2 = UsuarioVocacionalFactory(nome='João')
        database.session.add(pre_cadastro_2)
        database.session.flush()

    with mock_db_time(model=EtapaVocacional, time=datetime(2035, 3, 11)):
        etapa_2 = EtapaVocacionalFactory(
            fk_usuario_vocacional_id=pre_cadastro_2.id
        )
        database.session.add(etapa_2)
        database.session.commit()

    response = client.get(
        '/api/vocacional/listar-pre-cadastros?data_inicial=2035-03-10',
        headers={'Authorization': f'Bearer {membro_token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json['total'] == total_registros

    pre_cadastro = response.json['pre_cadastros'][0]['pre_cadastro']
    assert pre_cadastro['nome'] == 'João'


def test_busca_pre_cadastro_por_data_final(
    client: FlaskClient,
    membro_token,
    mock_db_time,
):
    total_registros = 1

    novo_pre_cadastro = UsuarioVocacionalFactory()
    database.session.add(novo_pre_cadastro)
    database.session.flush()

    etapa = EtapaVocacionalFactory(
        fk_usuario_vocacional_id=novo_pre_cadastro.id
    )
    database.session.add(etapa)
    database.session.commit()

    with mock_db_time(model=UsuarioVocacional, time=datetime(2023, 3, 11)):
        pre_cadastro_2 = UsuarioVocacionalFactory(nome='João')
        database.session.add(pre_cadastro_2)
        database.session.flush()

    with mock_db_time(model=EtapaVocacional, time=datetime(2023, 3, 11)):
        etapa_2 = EtapaVocacionalFactory(
            fk_usuario_vocacional_id=pre_cadastro_2.id
        )
        database.session.add(etapa_2)
        database.session.commit()

    response = client.get(
        '/api/vocacional/listar-pre-cadastros?data_final=2024-03-10',
        headers={'Authorization': f'Bearer {membro_token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json['total'] == total_registros

    pre_cadastro = response.json['pre_cadastros'][0]['pre_cadastro']
    assert pre_cadastro['nome'] == 'João'
