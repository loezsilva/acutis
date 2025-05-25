import uuid
from http import HTTPStatus

from flask.testing import FlaskClient


def test_alterar_vinculo_membro_oficial_sucesso(
    client: FlaskClient,
    seed_membros_oficial_general_status_dinamico,
    seed_membros_oficial_marechal_status_dinamico,
    membro_token,
):
    membro_general = seed_membros_oficial_general_status_dinamico(
        status='aprovado'
    )
    membro_marechal = seed_membros_oficial_marechal_status_dinamico(
        status='aprovado'
    )

    response = client.put(
        '/api/admin/membros-oficiais/alterar-vinculo',
        json={
            'fk_membro_oficial_id': membro_general.id,
            'fk_membro_superior_oficial_id': membro_marechal.id,
        },
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK


def test_alterar_vinculo_membro_oficial_nao_encontrado(
    client: FlaskClient,
    seed_membros_oficial_marechal_status_dinamico,
    membro_token,
):
    membro_marechal = seed_membros_oficial_marechal_status_dinamico(
        status='aprovado'
    )

    response = client.put(
        '/api/admin/membros-oficiais/alterar-vinculo',
        json={
            'fk_membro_oficial_id': str(uuid.uuid4()),
            'fk_membro_superior_oficial_id': membro_marechal.id,
        },
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json == [{'msg': 'Membro oficial não encontrado'}]


def test_alterar_vinculo_oficial_superior_nao_encontrado(
    client: FlaskClient,
    seed_membros_oficial_general_status_dinamico,
    membro_token,
):
    membro_general = seed_membros_oficial_general_status_dinamico(
        status='aprovado'
    )

    response = client.put(
        '/api/admin/membros-oficiais/alterar-vinculo',
        json={
            'fk_membro_oficial_id': membro_general.id,
            'fk_membro_superior_oficial_id': str(uuid.uuid4()),
        },
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json == [{'msg': 'Oficial superior não encontrado'}]


def test_alterar_vinculo_membro_oficial_a_si_mesmo(
    client: FlaskClient,
    seed_membros_oficial_general_status_dinamico,
    membro_token,
):
    membro_general = seed_membros_oficial_general_status_dinamico(
        status='aprovado'
    )

    response = client.put(
        '/api/admin/membros-oficiais/alterar-vinculo',
        json={
            'fk_membro_oficial_id': membro_general.id,
            'fk_membro_superior_oficial_id': membro_general.id,
        },
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json == [
        {'msg': 'Não é possível vincular oficial a ele mesmo'}
    ]


def test_alterar_vinculo_oficiais_com_mesmo_cargo(
    client: FlaskClient,
    seed_membros_oficial_status_dinamico,
    membro_token,
):
    membro_general = seed_membros_oficial_status_dinamico(status='aprovado')

    membro_superior = seed_membros_oficial_status_dinamico(status='aprovado')

    response = client.put(
        '/api/admin/membros-oficiais/alterar-vinculo',
        json={
            'fk_membro_oficial_id': membro_general.id,
            'fk_membro_superior_oficial_id': membro_superior.id,
        },
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json == [{'msg': 'Ambos oficiais possuem o mesmo cargo'}]
