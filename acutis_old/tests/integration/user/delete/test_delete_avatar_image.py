from flask.testing import FlaskClient
from flask_jwt_extended import create_access_token
from builder import db


def test_upload_avatar_image_success(
    test_client: FlaskClient, seed_benefector_user
):
    user = seed_benefector_user

    access_token = create_access_token(identity=user.id)

    response = test_client.delete(
        "/users/deletar-foto-perfil",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 204

    db.session.refresh(user)
    assert user.avatar is None
