import pytest

from acutis_api.infrastructure.extensions import database
from tests.factories import LeadFactory


@pytest.fixture
def seed_lead_inativo():
    lead = LeadFactory(status=False)
    lead.senha = '#Teste;@123'
    database.session.add(lead)
    database.session.commit()
    return lead


@pytest.fixture
def seed_lead_ativo():
    lead = LeadFactory(status=True)
    lead.senha = '#Teste;@123'
    database.session.add(lead)
    database.session.commit()
    return lead
