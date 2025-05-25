from unittest.mock import MagicMock
from faker import Faker
import pytest

from handlers.admin.get.get_all.get_all_actions import GetAllActions
from main import app


faker = Faker()


class MockQuery:
    def __init__(self) -> None:
        self.items = [
            MagicMock(
                id=1,
                nome=faker.name(),
                quantidade_leads=2,
                criada_em=faker.date(),
                status=True,
                sorteio=False,
            ),
            MagicMock(
                id=2,
                nome=faker.name(),
                quantidade_leads=5541,
                criada_em=faker.date(),
                status=False,
                sorteio=False,
            ),
        ]
        self.outerjoin = MagicMock(return_value=self)
        self.filter = MagicMock(return_value=self)
        self.group_by = MagicMock(return_value=self)
        self.order_by = MagicMock(return_value=self)
        self.total = 2
        self.paginate = MagicMock(
            return_value=MagicMock(items=self.items, total=self.total)
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
def get_all_actions(database):
    return GetAllActions(database)


def test_get_all_actions_success(get_all_actions, database):
    with app.test_request_context():
        _, status_code = get_all_actions.execute()

        assert status_code == 200

        session_mock = database.session
        query_mock = session_mock.query

        query_mock.assert_called_once()

        outerjoin_mock = query_mock.return_value.outerjoin
        outerjoin_mock.assert_called_once()

        filter_mock = query_mock.return_value.filter
        filter_mock.assert_called_once()

        group_by_mock = query_mock.return_value.group_by
        group_by_mock.assert_called_once()

        order_by_mock = query_mock.return_value.order_by
        order_by_mock.assert_called_once()

        paginate_mock = query_mock.return_value.paginate
        paginate_mock.assert_called_once()
