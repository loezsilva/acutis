from http import HTTPStatus

from flask.testing import FlaskClient


def test_listar_membros_oficiais_sucesso(
    client: FlaskClient, seed_membros_oficial, membro_token
):
    response = client.get(
        '/api/admin/membros-oficiais/listar',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK


def test_listar_membros_oficiais_nao_autorizado(
    client: FlaskClient, seed_membros_oficial
):
    response = client.get(
        '/api/admin/membros-oficiais/listar',
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_listar_membros_oficiais_filtro_dinamico(
    client: FlaskClient, seed_membros_oficial_status_dinamico, membro_token
):
    total_registros = 2
    seed_membros_oficial_status_dinamico(
        status='pendente',
        nome='Abrantes',
    )

    seed_membros_oficial_status_dinamico(
        status='aprovado',
        nome='Carlos Endente',
    )

    seed_membros_oficial_status_dinamico(
        status='recusado',
        nome='Carlos',
    )

    response = client.get(
        '/api/admin/membros-oficiais/listar?filtro_dinamico=endente',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json['total'] == total_registros
    membros_oficiais = response.json['membros_oficiais']
    assert any(membro['status'] == 'pendente' for membro in membros_oficiais)
    assert any(
        membro['nome'] == 'Carlos Endente' for membro in membros_oficiais
    )


def test_listar_membros_oficiais_filtro_dinamico_numero(
    client: FlaskClient, seed_membros_oficial_status_dinamico, membro_token
):
    total_registros = 1
    seed_membros_oficial_status_dinamico(
        status='pendente',
        numero_documento='2104456789',
    )

    seed_membros_oficial_status_dinamico(
        status='pendente',
        numero_documento='987654321',
    )

    response = client.get(
        '/api/admin/membros-oficiais/listar?filtro_dinamico=2104456',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json['total'] == total_registros
    membros_oficiais = response.json['membros_oficiais']
    assert any(
        membro['numero_documento'] == '2104456789'
        for membro in (membros_oficiais)
    )


def test_listar_membros_oficiais_filtro_dinamico_menos_4_caracteres(
    client: FlaskClient, membro_token
):
    response = client.get(
        '/api/admin/membros-oficiais/listar?filtro_dinamico=123',
        headers={'Authorization': f'Bearer {membro_token}'},
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_CONTENT
    assert response.json[0]['msg'] == (
        'Value error, O filtro dinâmico deve ter pelo menos 4 caracteres.'
    )
