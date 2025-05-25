from unittest.mock import MagicMock
from faker import Faker
import pytest

from handlers.admin.get.get_all.get_all_actions_names import GetAllActionsNames
from main import app


faker = Faker()


class MockQuery:
    def __init__(self) -> None:
        self.all = MagicMock(
            return_value=[
                MagicMock(id=1, nome=faker.name()),
                MagicMock(id=2, nome=faker.name()),
                MagicMock(id=3, nome=faker.name()),
            ]
        )


class MockSession:
    def __init__(self) -> None:
        self.query = MagicMock(return_value=MockQuery())


class MockDatabase:
    def __init__(self) -> None:
        self.session = MockSession()


@pytest.fixture
def database():
    return MockDatabase()


@pytest.fixture
def get_all_actions_names(database):
    return GetAllActionsNames(database)


def test_get_all_actions_names_success(get_all_actions_names, database):
    with app.test_request_context():
        _, status_code = get_all_actions_names.execute()

        assert status_code == 200

        session_mock = database.session
        query_mock = session_mock.query

        query_mock.assert_called_once()

        all_mock = query_mock.return_value.all
        all_mock.assert_called_once()
