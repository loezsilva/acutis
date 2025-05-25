
import pytest
from builder import db
from tests.integration.campaign.factories import CampaignFactory

@pytest.fixture
def seed_campaign():
    campanha = CampaignFactory()
    db.session.add(campanha)
    db.session.commit()
    db.session.flush()
    
    return campanha