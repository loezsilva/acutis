from http import HTTPStatus
from flask.testing import FlaskClient
from builder import db
from models.agape.membro_agape import MembroAgape


def test_delete_agape_family_success(
    test_client: FlaskClient,
    seed_admin_user_token,
    seed_agape_family_with_members,
):
    familia, membros = seed_agape_family_with_members
    membros_id = [membro.id for membro in membros]

    response = test_client.delete(
        f"/agape/deletar-familia/{familia.id}", headers=seed_admin_user_token
    )

    assert response.status_code == HTTPStatus.NO_CONTENT

    db.session.refresh(familia)
    assert familia.deleted_at is not None

    for membro_id in membros_id:
        db_membro = db.session.get(MembroAgape, membro_id)
        assert db_membro is None


def test_delete_agape_family_not_found(
    test_client: FlaskClient, seed_admin_user_token
):
    response = test_client.delete(
        "/agape/deletar-familia/9999", headers=seed_admin_user_token
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json == {"error": "Família não encontrada."}


def test_delete_agape_family_error_family_deleted(
    test_client: FlaskClient,
    seed_admin_user_token,
    seed_family_deleted,
):
    familia = seed_family_deleted

    response = test_client.delete(
        f"/agape/deletar-familia/{familia.id}", headers=seed_admin_user_token
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json == {"error": "Família não encontrada."}
