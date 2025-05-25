import uuid
from http import HTTPStatus

from flask.testing import FlaskClient


def test_alterar_status_membro_oficial_aprovar_sucesso(
    client: FlaskClient, seed_membros_oficial_status_dinamico, membro_token
):
    membro_oficial = seed_membros_oficial_status_dinamico(status='pendente')

    response = client.put(
        '/api/admin/membros-oficiais/alterar-status',
        json={
            'acao': 'aprovar',
            'fk_membro_oficial_id': str(membro_oficial.id),
        },
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.get_json() == {'msg': 'Oficial aprovado com sucesso'}


def test_alterar_status_membro_oficial_recusar_sucesso(
    client: FlaskClient, seed_membros_oficial_status_dinamico, membro_token
):
    membro_oficial = seed_membros_oficial_status_dinamico(status='pendente')

    response = client.put(
        '/api/admin/membros-oficiais/alterar-status',
        json={
            'acao': 'recusar',
            'fk_membro_oficial_id': str(membro_oficial.id),
        },
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.get_json() == {'msg': 'Oficial recusado com sucesso'}


def test_alterar_status_membro_oficial_nao_encontrado(
    client: FlaskClient, membro_token
):
    id_inexistente = uuid.uuid4()

    response = client.put(
        '/api/admin/membros-oficiais/alterar-status',
        json={'acao': 'aprovar', 'fk_membro_oficial_id': str(id_inexistente)},
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.get_json()[0] == {'msg': 'Membro oficial não encontrado'}


def test_aprovar_membro_oficial_ja_aprovado(
    client: FlaskClient, seed_membros_oficial_status_dinamico, membro_token
):
    membro_oficial = seed_membros_oficial_status_dinamico(status='aprovado')

    response = client.put(
        '/api/admin/membros-oficiais/alterar-status',
        json={
            'acao': 'aprovar',
            'fk_membro_oficial_id': str(membro_oficial.id),
        },
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.get_json()[0] == {'msg': 'Membro oficial já aprovado'}


def test_recusar_membro_oficial_ja_recusado(
    client: FlaskClient, seed_membros_oficial_status_dinamico, membro_token
):
    membro_oficial = seed_membros_oficial_status_dinamico(status='recusado')

    response = client.put(
        '/api/admin/membros-oficiais/alterar-status',
        json={
            'acao': 'recusar',
            'fk_membro_oficial_id': str(membro_oficial.id),
        },
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.get_json()[0] == {'msg': 'Membro oficial já recusado'}
