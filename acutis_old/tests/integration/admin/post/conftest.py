from faker import Faker
import pytest

from builder import db
from models.actions_leads import ActionsLeads
from models.foto_leads import FotoLeads
from models.leads_sorteados import LeadsSorteados
from models.users_imports import UsersImports
from utils.functions import get_current_time

faker = Faker("pt_BR")


@pytest.fixture
def seed_foto_leads():
    action = ActionsLeads(
        nome="Campanha Solidária",
    )
    db.session.add(action)
    db.session.flush()

    lead_1 = UsersImports(
        nome=faker.name(), email=faker.email(), origem_cadastro=action.id
    )
    db.session.add(lead_1)
    db.session.flush()

    lead_2 = UsersImports(
        nome=faker.name(), email=faker.email(), origem_cadastro=action.id
    )
    db.session.add(lead_2)
    db.session.flush()

    foto_1 = FotoLeads(
        fk_user_import_id=lead_1.id,
        user_download=None,
        data_download=None,
    )
    db.session.add(foto_1)

    foto_2 = FotoLeads(
        fk_user_import_id=lead_2.id,
        user_download=None,
        data_download=None,
    )
    db.session.add(foto_2)
    db.session.commit()

    return lead_1, lead_2, foto_1, foto_2


@pytest.fixture
def seed_actions_and_leads():
    action = ActionsLeads(
        nome="Ação de Teste",
        titulo="Título de Teste",
        descricao="Descrição de Teste",
        status=True,
        sorteio=False,
        created_at=get_current_time(),
    )

    lead = LeadsSorteados(
        nome="Lead de Teste",
        email="lead@headers.com.br",
        data_sorteio=None,
        sorteador=None,
        acao_sorteada=None,
    )
    db.session.add(action)
    db.session.add(lead)
    db.session.commit()
    return action, lead
