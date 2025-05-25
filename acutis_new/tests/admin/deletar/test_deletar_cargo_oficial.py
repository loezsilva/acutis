import uuid
from http import HTTPStatus

from flask.testing import FlaskClient

from acutis_api.domain.entities.cargo_oficial import CargosOficiais
from acutis_api.domain.entities.oficial import Oficial
from acutis_api.infrastructure.extensions import database


def test_excluir_cargo_oficial_sucesso(
    client: FlaskClient,
    seed_membros_oficial_general_status_dinamico,
    membro_token,
):
    membro_oficial_1 = seed_membros_oficial_general_status_dinamico(
        status='aprovado'
    )
    membro_oficial_2 = seed_membros_oficial_general_status_dinamico(
        status='aprovado'
    )

    response = client.delete(
        f'/api/admin/cargos-oficiais/excluir/{membro_oficial_2.fk_cargo_oficial_id}',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json == {'msg': 'Cargo oficial deletado com sucesso.'}

    cargo_excluido = (
        database.session.query(CargosOficiais)
        .filter_by(id=membro_oficial_2.fk_cargo_oficial_id)
        .first()
    )
    assert cargo_excluido is None

    membro_oficial_1_atualizado = (
        database.session.query(Oficial)
        .filter_by(id=membro_oficial_1.id)
        .first()
    )
    membro_oficial_2_atualizado = (
        database.session.query(Oficial)
        .filter_by(id=membro_oficial_2.id)
        .first()
    )

    assert membro_oficial_1_atualizado.fk_cargo_oficial_id is None
    assert membro_oficial_2_atualizado.fk_cargo_oficial_id is None


def test_excluir_cargo_oficial_nao_encontrado(
    client: FlaskClient,
    membro_token,
):
    id_inexistente = uuid.uuid4()

    response = client.delete(
        f'/api/admin/cargos-oficiais/excluir/{id_inexistente}',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json == [{'msg': 'Cargo oficial não encontrado'}]


def test_excluir_cargo_oficial_nao_autorizado(
    client: FlaskClient,
):
    id_inexistente = uuid.uuid4()

    response = client.delete(
        f'/api/admin/cargos-oficiais/excluir/{id_inexistente}',
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
