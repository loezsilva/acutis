from flask.testing import FlaskClient
from builder import db


def test_update_action_status_success(
    test_client: FlaskClient, seed_action, seed_admin_user_token
):
    action = seed_action
    initial_status = action.status

    response = test_client.patch(
        f"/administradores/editar-status-acao/{action.id}",
        headers=seed_admin_user_token,
    )

    assert response.status_code == 204

    db.session.refresh(action)
    assert action.status != initial_status
