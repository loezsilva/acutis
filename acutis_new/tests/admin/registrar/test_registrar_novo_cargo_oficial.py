import json
from http import HTTPStatus

from flask.testing import FlaskClient


def test_registrar_novo_cargo_oficial(client: FlaskClient, membro_token):
    response = client.post(
        '/api/admin/cargos-oficiais/registrar',
        headers={'Authorization': f'Bearer {membro_token}'},
        data=json.dumps({
            'nome_cargo': 'General',
            'fk_cargo_superior_id': None,
        }),
        content_type='application/json',
    )

    assert response.status_code == HTTPStatus.CREATED
    data = response.get_json()

    assert data['nome_cargo'] == 'General'
    assert 'id' in data


def test_registrar_cargo_oficial_error(client: FlaskClient, membro_token):
    response = client.post(
        '/api/admin/cargos-oficiais/registrar',
        headers={'Authorization': f'Bearer {membro_token}'},
        data=json.dumps({'nome_cargo': 'Gen', 'fk_cargo_superior_id': None}),
        content_type='application/json',
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    data = response.get_json()
    assert data[0]['msg'] == 'Nome do cargo deve ter mínimo de 4 caracteres'


def test_registrar_cargo_oficial_coflict_error(
    client: FlaskClient, membro_token, seed_cargo_oficial
):
    cargo_oficial = seed_cargo_oficial

    response = client.post(
        '/api/admin/cargos-oficiais/registrar',
        headers={'Authorization': f'Bearer {membro_token}'},
        data=json.dumps({
            'nome_cargo': cargo_oficial.nome_cargo,
            'fk_cargo_superior_id': None,
        }),
        content_type='application/json',
    )

    assert response.status_code == HTTPStatus.CONFLICT
    data = response.get_json()
    assert data[0]['msg'] == 'Já existe um cargo com este nome.'


def test_registrar_novo_cargo_oficial_com_superior(
    client: FlaskClient, membro_token, seed_cargo_oficial
):
    response = client.post(
        '/api/admin/cargos-oficiais/registrar',
        headers={'Authorization': f'Bearer {membro_token}'},
        data=json.dumps({
            'nome_cargo': 'Cargo com superior',
            'fk_cargo_superior_id': str(seed_cargo_oficial.id),
        }),
        content_type='application/json',
    )

    assert response.status_code == HTTPStatus.CREATED
    data = response.get_json()

    assert data['nome_cargo'] == 'Cargo com superior'
    assert 'id' in data
