from faker import Faker
import pytest

from models.clifor import Clifor
from models.endereco import Endereco
from models.usuario import Usuario
from builder import db

faker = Faker("pt_BR")


@pytest.fixture
def seed_user_to_admin_update():
    nome = faker.name()
    email = faker.email(domain="headers.com.br")

    user = Usuario(
        nome=nome,
        email=email,
        country="uruguai",
        status=True,
        usuario_criacao=0,
    )
    db.session.add(user)
    db.session.flush()

    clifor = Clifor(
        fk_usuario_id=user.id,
        nome=nome,
        email=email,
        cpf_cnpj="12345678901",
        telefone1="(11) 98765-4321",
        usuario_criacao=0,
    )
    db.session.add(clifor)
    db.session.flush()

    db.session.commit()

    return user, clifor


@pytest.fixture
def seed_user_to_test_edit_address():
    nome = faker.name()
    email = faker.email(domain="headers.com.br")

    user = Usuario(nome=nome, email=email)
    db.session.add(user)
    db.session.flush()

    clifor = Clifor(fk_usuario_id=user.id)
    db.session.add(clifor)
    db.session.flush()

    address = Endereco(
        fk_clifor_id=clifor.id,
        cep="77018468",
        rua="Quadra Sul Alameda",
        numero="1240",
        bairro="Plano Diretor Sul",
        cidade="Palmas",
        estado="TO",
    )
    db.session.add(address)
    db.session.commit()

    return user, address
