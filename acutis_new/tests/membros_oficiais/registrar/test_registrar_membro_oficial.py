import json
import uuid
from http import HTTPStatus

from flask.testing import FlaskClient

from acutis_api.domain.entities.oficial import Oficial
from acutis_api.infrastructure.extensions import database


def test_registrar_membro_oficial_com_sucesso(
    client: FlaskClient,
    seed_membros_oficial,
    seed_cargo_oficial,
    seed_registrar_membro,
):
    membro_nao_oficial = seed_registrar_membro()[1]

    membro_oficial = seed_membros_oficial[0]

    payload = {
        'fk_membro_id': str(membro_nao_oficial.id),
        'fk_superior_id': str(membro_oficial.fk_membro_id),
        'fk_cargo_oficial_id': str(seed_cargo_oficial.id),
    }

    response = client.post(
        '/api/membros-oficiais/registrar',
        data=json.dumps(payload),
        content_type='application/json',
    )

    oficial_cadastrado = (
        database.session.query(Oficial)
        .filter(Oficial.id == response.get_json()['uuid'])
        .first()
    )

    assert response.status_code == HTTPStatus.CREATED
    assert oficial_cadastrado.status == 'pendente'


def test_registrar_membro_oficial_sem_superior_com_sucesso(
    client: FlaskClient, seed_cargo_oficial, seed_registrar_membro
):
    membro_nao_oficial = seed_registrar_membro()[1]

    payload = {
        'fk_membro_id': str(membro_nao_oficial.id),
        'fk_superior_id': None,
        'fk_cargo_oficial_id': str(seed_cargo_oficial.id),
    }

    response = client.post(
        '/api/membros-oficiais/registrar',
        data=json.dumps(payload),
        content_type='application/json',
    )

    oficial_cadastrado = (
        database.session.query(Oficial)
        .filter(Oficial.id == response.get_json()['uuid'])
        .first()
    )

    assert response.status_code == HTTPStatus.CREATED
    assert oficial_cadastrado.status == 'pendente'


def test_registrar_membro_oficial_bad_request_error(
    client: FlaskClient, seed_registrar_membro, seed_cargo_oficial
):
    membro = seed_registrar_membro()[1]

    payload = {
        'fk_membro_id': str(membro.id),
        'fk_superior_id': str(membro.id),
        'fk_cargo_oficial_id': str(seed_cargo_oficial.id),
    }

    response = client.post(
        '/api/membros-oficiais/registrar',
        data=json.dumps(payload),
        content_type='application/json',
    )

    data = response.get_json()[0]

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert data == {'msg': 'Não é possível vincular-se a se mesmo.'}


def test_registrar_membro_oficial_ja_cadastrado(
    client: FlaskClient, seed_membros_oficial, seed_cargo_oficial
):
    membro_oficial_1 = seed_membros_oficial[0]
    membro_oficial_2 = seed_membros_oficial[1]

    payload = {
        'fk_membro_id': str(membro_oficial_1.fk_membro_id),
        'fk_superior_id': str(membro_oficial_2.fk_membro_id),
        'fk_cargo_oficial_id': str(seed_cargo_oficial.id),
    }

    response = client.post(
        '/api/membros-oficiais/registrar',
        data=json.dumps(payload),
        content_type='application/json',
    )

    assert response.status_code == HTTPStatus.CONFLICT
    data = response.get_json()

    assert data[0] == {'msg': 'Esse membro já é um membro oficial.'}


def test_registrar_membro_oficial_sem_cadastro_de_membro(
    client: FlaskClient,
    seed_membros_oficial,
    seed_cargo_oficial,
):
    id_membro_inexistente = uuid.uuid4()
    membro_oficial = seed_membros_oficial[0]

    payload = {
        'fk_membro_id': str(id_membro_inexistente),
        'fk_superior_id': str(membro_oficial.fk_membro_id),
        'fk_cargo_oficial_id': str(seed_cargo_oficial.id),
    }

    response = client.post(
        '/api/membros-oficiais/registrar',
        data=json.dumps(payload),
        content_type='application/json',
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.get_json() == [
        {'msg': 'É necessário ter o cadastro de membro'}
    ]
