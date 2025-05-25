from unittest.mock import MagicMock

from faker import Faker
import pytest

from handlers.admin.get.get_by_id.get_profile_by_id import GetProfileById
from main import app


faker = Faker(locale="pt_BR")


class MockQuery:
    def __init__(self):
        self.join = MagicMock(return_value=self)
        self.filter = MagicMock(return_value=self)
        self.first = MagicMock(
            return_value=MagicMock(
                id=1,
                nome=faker.name(),
                status=True,
                super_perfil=True,
                data_criacao=faker.date(),
            )
        )
        self.all = MagicMock(
            return_value=[
                MagicMock(
                    fk_menu_id=1,
                    acessar=1,
                    criar=1,
                    editar=1,
                    deletar=1,
                    nome_menu=faker.name(),
                ),
                MagicMock(
                    fk_menu_id=2,
                    acessar=0,
                    criar=1,
                    editar=0,
                    deletar=1,
                    nome_menu=faker.name(),
                ),
            ]
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
def get_profile_by_id(database):
    return GetProfileById(database)


def test_get_profile_by_id_success(get_profile_by_id, database):
    with app.test_request_context():
        _, status_code = get_profile_by_id.execute(1)

        assert status_code == 200

        session_mock = database.session
        query_mock = session_mock.query

        query_mock.assert_called()

        filter_mock = query_mock.return_value.filter
        filter_mock.assert_called()
        filter_mock.assert_called()

        first_mock = query_mock.return_value.first
        first_mock.assert_called_once()

        all_mock = query_mock.return_value.all
        all_mock.assert_called_once()
