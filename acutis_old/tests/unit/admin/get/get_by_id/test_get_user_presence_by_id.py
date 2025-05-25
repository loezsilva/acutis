from unittest.mock import MagicMock
import pytest
from handlers.admin.get.get_by_id.get_user_presence_by_id import GetUserPresenceById
from main import app


class MockQuery:
    def __init__(self):
        self.filter_by = MagicMock(return_value=self)
        self.all = MagicMock(
            return_value=[
                MagicMock(presencas=7),
                MagicMock(presencas=3),
                MagicMock(presencas=5),
            ]
        )


class MockSession:
    def __init__(self):
        self.get = MagicMock()
        self.query = MagicMock(return_value=MockQuery())


class MockDatabase:
    def __init__(self):
        self.session = MockSession()


@pytest.fixture
def database():
    return MockDatabase()


@pytest.fixture
def get_user_presence_by_id(database):
    return GetUserPresenceById(database)


def test_get_user_presence_by_id_success(get_user_presence_by_id, database):
    with app.test_request_context():
        _, status_code = get_user_presence_by_id.execute(1)

        assert status_code == 200

        session_mock = database.session
        query_mock = session_mock.query

        query_mock.assert_called_once()

        filter_by_mock = query_mock.return_value.filter_by
        filter_by_mock.assert_called_once()

        all_mock = query_mock.return_value.all
        all_mock.assert_called_once()
