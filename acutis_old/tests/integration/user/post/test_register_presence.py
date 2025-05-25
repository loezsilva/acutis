from faker import Faker
from flask.testing import FlaskClient
from flask_jwt_extended import create_access_token
from builder import db
from models import Campanha, EventoUsuario

faker = Faker("pt_BR")


def test_register_presence_success(
    test_client: FlaskClient, seed_benefector_user
):
    user = seed_benefector_user
    campaign = Campanha(
        titulo=faker.name(), status=True, publica=True, usuario_criacao=0
    )
    db.session.add(campaign)
    db.session.commit()

    payload = {
        "fk_campanha_id": campaign.id,
    }
    access_token = create_access_token(identity=user.id)

    response = test_client.post(
        "/users/registrar-presenca",
        json=payload,
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 201
    data = response.get_json()
    assert data["msg"] == "Presença registrada com sucesso!"

    presence = EventoUsuario.query.filter_by(
        fk_usuario_id=user.id, fk_campanha_id=campaign.id
    ).first()
    assert presence is not None
    assert presence.fk_usuario_id == user.id
    assert presence.fk_campanha_id == campaign.id

    db.session.delete(presence)
    db.session.delete(campaign)
    db.session.commit()
