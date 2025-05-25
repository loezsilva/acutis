from unittest.mock import MagicMock
from faker import Faker
from werkzeug.datastructures import MultiDict
import pytest

from handlers.admin.get.get_all.get_all_profiles import GetAllProfiles
from main import app


faker = Faker()


class MockQuery:
    def __init__(self) -> None:
        self.items = [
            MagicMock(
                id=1,
                nome=faker.name(),
                status=True,
                super_perfil=True,
                data_criacao=faker.date(),
                quantidade_usuarios=50,
            ),
            MagicMock(
                id=2,
                nome=faker.name(),
                status=True,
                super_perfil=True,
                data_criacao=faker.date(),
                quantidade_usuarios=170,
            ),
        ]
        self.total = 2
        self.outerjoin = MagicMock(return_value=self)
        self.group_by = MagicMock(return_value=self)
        self.order_by = MagicMock(return_value=self)
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
def get_all_profiles(database):
    return GetAllProfiles(database)


def test_get_all_profiles_sucess(get_all_profiles, database):
    args = MultiDict(
        [
            ("page", 1),
            ("per_page", 5),
        ]
    )

    with app.test_request_context(query_string=args):
        _, status_code = get_all_profiles.execute()

        assert status_code == 200

        session_mock = database.session
        query_mock = session_mock.query

        query_mock.assert_called_once()

        outerjoin_mock = query_mock.return_value.outerjoin
        outerjoin_mock.assert_called_once()

        group_by_mock = query_mock.return_value.group_by
        group_by_mock.assert_called_once()

        order_by_mock = query_mock.return_value.order_by
        order_by_mock.assert_called_once()

        paginate_mock = query_mock.return_value.paginate
        paginate_mock.assert_called_once()
