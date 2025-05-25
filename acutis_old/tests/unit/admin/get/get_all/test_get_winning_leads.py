from unittest.mock import MagicMock
from faker import Faker
from werkzeug.datastructures import MultiDict
import pytest
from handlers.admin.get.get_all.get_winning_leads import GetWinningLeads
from main import app

faker = Faker()


class MockQuery:
    def __init__(self):
        self.items = [
            MagicMock(
                id=1,
                nome=faker.name(),
                email=faker.email(),
                data_sorteio=faker.date(),
                tel=faker.phone_number(),
            ),
            MagicMock(
                id=2,
                nome=faker.name(),
                email=faker.email(),
                data_sorteio=faker.date(),
                tel=faker.phone_number(),
            ),
        ]
        self.total = 2
        self.filter = MagicMock(return_value=self)
        self.join = MagicMock(return_value=self)
        self.order_by = MagicMock(return_value=self)
        self.paginate = MagicMock(
            return_value=MagicMock(items=self.items, total=self.total)
        )


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
def get_winning_leads(database):
    return GetWinningLeads(database)


def test_get_winning_leads_success(get_winning_leads, database):
    args = MultiDict(
        [
            ("page", 1),
            ("per_page", 5),
            ("filtro_acao_id", None),
        ]
    )

    with app.test_request_context(query_string=args):
        _, status_code = get_winning_leads.execute()

        assert status_code == 200

        session_mock = database.session
        query_mock = session_mock.query

        query_mock.assert_called_once()

        join_mock = query_mock.return_value.join
        join_mock.assert_called_once()

        filter_mock = query_mock.return_value.filter
        filter_mock.assert_called_once()

        order_by_mock = query_mock.return_value.order_by
        order_by_mock.assert_called_once()

        paginate_mock = query_mock.return_value.paginate
        paginate_mock.assert_called_once()
