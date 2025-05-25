from models.mensageria.tipo_email import TipoEmail
from flask.testing import FlaskClient
from builder import db
from faker import Faker

def test_create_new_type_email_success(test_client: FlaskClient, seed_admin_user_token):
    
    fake = Faker("pt_BR")
    
    random_email_type = f"{fake.bs().capitalize()} E-mail"
    
    payload = {"tipo_email": f"{random_email_type}"}

    response = test_client.post(
        "/mensageria/create-type-email",
        json=payload,
        headers=seed_admin_user_token,
    )

    assert response.status_code == 201

    data = response.get_json()
    assert data["msg"] == "Tipo de e-mail criado com sucesso!"   

    type_email = db.session.query(TipoEmail).filter_by(slug=random_email_type).first()
    
    assert type_email is not None
    assert type_email.slug == random_email_type