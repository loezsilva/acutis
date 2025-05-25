from unittest.mock import MagicMock
import pytest
from handlers.admin.get.get_by_id.get_total_leads_by_action_id import (
    GetTotalLeadsByActionId,
)
from main import app


class MockQuery:
    def __init__(self):
        self.filter = MagicMock(return_value=self)
        self.count = MagicMock(return_value=10)


class MockSession:
    def __init__(self):
        self.query = MagicMock(return_value=MockQuery())


class MockDatabase:
    def __init__(self):
        self.session = MockSession()


@pytest.fixture
def database():
    return MockDatabase()


@pytest.fixture
def get_total_leads_by_action_id(database):
    return GetTotalLeadsByActionId(database)


def test_get_total_leads_success(get_total_leads_by_action_id, database):
    with app.test_request_context():
        _, status_code = get_total_leads_by_action_id.execute(fk_acao_id=1)

        assert status_code == 200

        session_mock = database.session
        query_mock = session_mock.query

        query_mock.assert_called_once()
        filter_mock = query_mock.return_value.filter
        filter_mock.assert_called_once()

        count_mock = query_mock.return_value.count
        count_mock.assert_called_once()
