import json
import uuid
from http import HTTPStatus

from flask.testing import FlaskClient

from acutis_api.domain.entities.cargo_oficial import CargosOficiais
from acutis_api.infrastructure.extensions import database


def test_atualizar_cargo_oficial(
    client: FlaskClient, membro_token, seed_cargo_oficial
):
    response = client.put(
        f'/api/admin/cargos-oficiais/atualizar/{seed_cargo_oficial.id}',
        headers={'Authorization': f'Bearer {membro_token}'},
        data=json.dumps({
            'nome_cargo': 'Oficial Cargo',
            'fk_cargo_superior_id': None,
        }),
        content_type='application/json',
    )

    assert response.status_code == HTTPStatus.OK

    cargo_atualizado = (
        database.session.query(CargosOficiais)
        .filter(CargosOficiais.id == seed_cargo_oficial.id)
        .first()
    )

    assert cargo_atualizado.nome_cargo == 'Oficial Cargo'


def test_atualizar_cargo_oficial_conflict_error(
    client: FlaskClient, membro_token, seed_3_cargos_oficiais
):
    cargo1 = seed_3_cargos_oficiais[0]
    cargo2 = seed_3_cargos_oficiais[1]

    response = client.put(
        f'/api/admin/cargos-oficiais/atualizar/{cargo1.id}',
        headers={'Authorization': f'Bearer {membro_token}'},
        data=json.dumps({
            'nome_cargo': f'{cargo2.nome_cargo}',
            'fk_cargo_superior_id': cargo2.fk_cargo_superior_id,
        }),
        content_type='application/json',
    )

    data = response.get_json()[0]

    assert response.status_code == HTTPStatus.CONFLICT
    assert data == {'msg': 'Já existe um cargo com mesmo nome'}


def test_atualizar_cargo_oficial_nao_autorizado(
    client: FlaskClient, seed_cargo_oficial
):
    response = client.put(
        f'/api/admin/cargos-oficiais/atualizar/{seed_cargo_oficial.id}',
        data=json.dumps({
            'nome_cargo': 'Oficial Cargo',
            'fk_cargo_superior_id': None,
        }),
        content_type='application/json',
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_atualizar_cargo_oficial_not_found(client: FlaskClient, membro_token):
    id_cargo_oficial = uuid.uuid4()

    response = client.put(
        f'/api/cargos-oficiais/atualizar/{id_cargo_oficial}',
        headers={'Authorization': f'Bearer {membro_token}'},
        data=json.dumps({
            'nome_cargo': 'Oficial Cargo',
            'fk_cargo_superior_id': None,
        }),
        content_type='application/json',
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_atualizar_cargo_oficial_com_cargo_superior(
    client: FlaskClient, membro_token, seed_3_cargos_oficiais
):
    cargo1 = seed_3_cargos_oficiais[0]
    cargo2 = seed_3_cargos_oficiais[1]

    response = client.put(
        f'/api/admin/cargos-oficiais/atualizar/{cargo1.id}',
        headers={'Authorization': f'Bearer {membro_token}'},
        data=json.dumps({
            'nome_cargo': 'Oficial Cargo',
            'fk_cargo_superior_id': str(cargo2.id),
        }),
        content_type='application/json',
    )

    assert response.status_code == HTTPStatus.OK

    cargo_atualizado = (
        database.session.query(CargosOficiais)
        .filter(CargosOficiais.id == cargo1.id)
        .first()
    )

    assert cargo_atualizado.nome_cargo == 'Oficial Cargo'
    assert cargo_atualizado.fk_cargo_superior_id == cargo2.id
