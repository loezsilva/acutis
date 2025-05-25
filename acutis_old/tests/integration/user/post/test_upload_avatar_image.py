from io import BytesIO
from flask.testing import FlaskClient
from flask_jwt_extended import create_access_token
from builder import db


def test_upload_avatar_image_success(
    test_client: FlaskClient, seed_benefector_user
):
    user = seed_benefector_user

    access_token = create_access_token(identity=user.id)
    avatar_image = (BytesIO(b"fake image data"), "avatar.jpg")

    response = test_client.post(
        "/users/salvar-foto-perfil",
        data={
            "image": avatar_image,
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200
    assert response.get_json() == {
        "msg": "Foto de perfil atualizada com sucesso!"
    }

    db.session.refresh(user)
    assert user.avatar is not None
    assert user.avatar == "avatar.jpg"
