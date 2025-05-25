from faker import Faker
from unittest.mock import MagicMock

import pytest

from handlers.admin.get.get_all.get_all_users import GetAllUsers
from main import app


faker = Faker()


class MockQuery:
    def __init__(self) -> None:
        self.items = [
            MagicMock(
                id=1, nome=faker.name(), email=faker.email(), status=True, data_criacao=faker.date_time()
            ),
            MagicMock(
                id=2, nome=faker.name(), email=faker.email(), status=True, data_criacao=faker.date_time()
            ),
        ]
        self.total = 2
        self.join = MagicMock(return_value=self)
        self.outerjoin = MagicMock(return_value=self)
        self.filter = MagicMock(return_value=self)
        self.order_by = MagicMock(return_value=self)
        self.paginate = MagicMock(
            return_value=MagicMock(items=self.items, total=self.total)
        )


class MockSession:
    def __init__(self) -> None:
        self.query = MagicMock(return_value=MockQuery())


class MockDatabase:
    def __init__(self):
        self.session = MockSession()


@pytest.fixture
def database():
    return MockDatabase()


@pytest.fixture
def get_all_users(database):
    return GetAllUsers(database)


def test_get_all_users_success(get_all_users, database):
    with app.test_request_context():
        _, status_code = get_all_users.execute()

        assert status_code == 200

        session_mock = database.session
        query_mock = session_mock.query

        query_mock.assert_called_once()

        filter_mock = query_mock.return_value.filter
        filter_mock.assert_called_once()

        order_by_mock = query_mock.return_value.order_by
        order_by_mock.assert_called_once()

        paginate_mock = query_mock.return_value.paginate
        paginate_mock.assert_called_once()
