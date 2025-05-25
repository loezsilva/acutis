from http import HTTPStatus
from flask.testing import FlaskClient

from builder import db

from models.agape.membro_agape import MembroAgape


def test_delete_agape_member_success(
    test_client: FlaskClient, seed_admin_user_token, seed_agape_member
):
    membro = seed_agape_member
    membro_id = membro.id

    response = test_client.delete(
        f"/agape/deletar-membro/{membro_id}", headers=seed_admin_user_token
    )

    assert response.status_code == HTTPStatus.NO_CONTENT

    db_membro = db.session.get(MembroAgape, membro_id)
    assert db_membro is None
