from faker import Faker
import pytest
from builder import db
from models.usuario import Usuario

faker = Faker("pt_BR")


@pytest.fixture
def create_test_user():
    nome = faker.name()
    email = faker.email(domain="headers.com.br")

    user = Usuario(
        nome=nome,
        email=email,
        password="Senha123",
        status=True,
    )
    db.session.add(user)
    db.session.commit()
    return user
