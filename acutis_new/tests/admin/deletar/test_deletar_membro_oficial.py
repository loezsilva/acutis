import uuid
from http import HTTPStatus

from flask.testing import FlaskClient

from acutis_api.domain.entities.oficial import Oficial
from acutis_api.infrastructure.extensions import database


def test_excluir_membro_oficial_sucesso(
    client: FlaskClient,
    seed_membros_oficial_general_status_dinamico,
    membro_token,
):
    membro_oficial = seed_membros_oficial_general_status_dinamico(
        status='aprovado'
    )

    response = client.delete(
        f'/api/admin/membros-oficiais/excluir/{membro_oficial.id}',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json == {'msg': 'Membro Oficial deletado com sucesso'}


def test_excluir_membro_oficial_nao_encontrado(
    client: FlaskClient,
    membro_token,
):
    id_inexistente = uuid.uuid4()

    response = client.delete(
        f'/api/admin/membros-oficiais/excluir/{id_inexistente}',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json == [{'msg': 'Membro oficial não encontrado'}]


def test_excluir_membro_oficial_remove_vinculo_superior(
    client: FlaskClient,
    seed_membros_oficial_general_com_superior,
    membro_token,
):
    marechal = seed_membros_oficial_general_com_superior

    vinculos = (
        database.session.query(Oficial)
        .filter(Oficial.fk_superior_id == marechal.fk_membro_id)
        .all()
    )

    assert len(vinculos) > 0

    response = client.delete(
        f'/api/admin/membros-oficiais/excluir/{marechal.id}',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json == {'msg': 'Membro Oficial deletado com sucesso'}

    vinculos_atualizado = (
        database.session.query(Oficial)
        .filter(Oficial.fk_superior_id == marechal.id)
        .all()
    )

    assert len(vinculos_atualizado) == 0
