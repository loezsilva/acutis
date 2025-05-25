from faker import Faker
import pytest
from models.actions_leads import ActionsLeads
from models.usuario import Usuario
from builder import db
from utils.functions import get_current_time

faker = Faker("pt_BR")


@pytest.fixture
def seed_test_user():
    user = Usuario(
        nome=faker.name(),
        email=faker.email(domain="headers.com.br"),
        status=False,
    )
    db.session.add(user)
    db.session.commit()

    return user


@pytest.fixture
def seed_action():
    action = ActionsLeads(
        nome=faker.name(),
        titulo="Título Original",
        descricao="Descrição original da campanha.",
        background="original_background.jpg",
        banner="original_banner.jpg",
        status=True,
        sorteio=False,
        preenchimento_foto=False,
        label_foto=None,
        created_at=get_current_time(),
    )

    db.session.add(action)
    db.session.commit()

    return action
