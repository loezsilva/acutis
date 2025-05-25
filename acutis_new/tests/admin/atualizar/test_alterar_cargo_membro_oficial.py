import uuid
from http import HTTPStatus

from flask.testing import FlaskClient


def test_alterar_cargo_membro_oficial_sucesso(
    client: FlaskClient,
    seed_cargo_oficial_marechal,
    seed_membros_oficial_status_dinamico,
    membro_token,
):
    cargo_oficial = seed_cargo_oficial_marechal
    membro_oficial = seed_membros_oficial_status_dinamico(status='pendente')

    response = client.put(
        '/api/admin/membros-oficiais/alterar-cargo',
        json={
            'fk_membro_oficial': str(membro_oficial.id),
            'fk_cargo_oficial_id': str(cargo_oficial.id),
        },
        headers={'Authorization': f'Bearer {membro_token}'},
    )
    assert response.status_code == HTTPStatus.OK

    assert response.get_json() == {
        'msg': 'Cargo do oficial alterado com sucesso.'
    }


def test_alterar_cargo_membro_oficial_nao_autorizado(
    client: FlaskClient,
    seed_membros_oficial_status_dinamico,
    seed_cargo_oficial,
):
    membro_oficial = seed_membros_oficial_status_dinamico(status='pendente')

    cargo_oficial = seed_cargo_oficial

    response = client.put(
        '/api/admin/membros-oficiais/alterar-cargo',
        json={
            'fk_membro_oficial': str(membro_oficial.id),
            'fk_cargo_oficial_id': str(cargo_oficial.id),
        },
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_alterar_cargo_membro_oficial_nao_encontrado(
    client: FlaskClient, seed_cargo_oficial, membro_token
):
    cargo_oficial = seed_cargo_oficial

    id_membro_inexistente = uuid.uuid4()

    response = client.put(
        '/api/admin/membros-oficiais/alterar-cargo',
        json={
            'fk_membro_oficial': str(id_membro_inexistente),
            'fk_cargo_oficial_id': str(cargo_oficial.id),
        },
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.get_json()[0] == {'msg': 'Membro oficial não encontrado'}


def test_alterar_cargo_cargo_oficial_nao_encontrado(
    client: FlaskClient, seed_membros_oficial_status_dinamico, membro_token
):
    membro_oficial = seed_membros_oficial_status_dinamico(status='aprovado')

    id_cargo_inexistente = uuid.uuid4()

    response = client.put(
        '/api/admin/membros-oficiais/alterar-cargo',
        json={
            'fk_membro_oficial': str(membro_oficial.id),
            'fk_cargo_oficial_id': str(id_cargo_inexistente),
        },
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.get_json() == [{'msg': 'Cargo oficial não encontrado'}]


def test_alterar_cargo_sem_cargo_oficial(
    client: FlaskClient, seed_membros_oficial_status_dinamico, membro_token
):
    membro_oficial = seed_membros_oficial_status_dinamico(status='aprovado')

    response = client.put(
        '/api/admin/membros-oficiais/alterar-cargo',
        json={
            'fk_membro_oficial': str(membro_oficial.id),
            'fk_cargo_oficial_id': None,
        },
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_CONTENT


def test_alterar_cargo_membro_oficial_ja_possui_cargo(
    client: FlaskClient, seed_membros_oficial_status_dinamico, membro_token
):
    membro_oficial = seed_membros_oficial_status_dinamico(status='aprovado')

    response = client.put(
        '/api/admin/membros-oficiais/alterar-cargo',
        json={
            'fk_membro_oficial': str(membro_oficial.id),
            'fk_cargo_oficial_id': str(membro_oficial.fk_cargo_oficial_id),
        },
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.get_json() == [
        {'msg': 'Membro Oficial já possui este cargo.'}
    ]
