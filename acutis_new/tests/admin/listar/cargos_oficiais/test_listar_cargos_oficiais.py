from http import HTTPStatus

from flask.testing import FlaskClient


def test_listar_todos_cargos_oficiais(
    client: FlaskClient, membro_token, seed_cargo_oficial
):
    response = client.get(
        '/api/admin/cargos-oficiais/listar-todos-cargos',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK


def test_listar_todos_cargos_oficiais_filtrando_por_id(
    client: FlaskClient, membro_token, seed_cargo_oficial
):
    response = client.get(
        f'/api/admin/cargos-oficiais/listar-todos-cargos?id={seed_cargo_oficial.id}',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK


def test_listar_todos_cargos_oficiais_filtrando_por_nome(
    client: FlaskClient, membro_token, seed_cargo_oficial
):
    response = client.get(
        f'/api/admin/cargos-oficiais/listar-todos-cargos?nome_cargo={
            seed_cargo_oficial.nome_cargo
        }',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK


def test_listar_de_cargos_oficiais(
    client: FlaskClient, membro_token, seed_cargo_oficial
):
    response = client.get(
        '/api/admin/cargos-oficiais/lista-de-cargos-oficiais',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    data = response.get_json()
    assert data == [
        {
            'id': str(seed_cargo_oficial.id),
            'nome_cargo': seed_cargo_oficial.nome_cargo,
        }
    ]
