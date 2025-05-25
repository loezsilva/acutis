from unittest.mock import MagicMock

from faker import Faker
import pytest
from werkzeug.datastructures import MultiDict


from handlers.admin.get.get_all.get_all_birthdays import GetAllBirthdays
from main import app

faker = Faker("pt_BR")


class MockQuery:
    def __init__(self) -> None:
        self.items = [
            MagicMock(
                id=1,
                foto="test.png",
                nome="Osvaldo Antonio Giovanni Lima",
                email="osvaldo_lima@viavaleseguros.com.br",
                data_nascimento="02/05/1990",
                telefone="92993032078",
            ),
            MagicMock(
                id=2,
                foto=None,
                nome="Alice Laura Novaes",
                email="alice-novaes96@azulcargo.com.br",
                data_nascimento="02/06/1946",
                telefone="68999990445",
            ),
        ]
        self.total = 2
        self.join = MagicMock(return_value=self)
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


class MockMinioClient:
    def get_public_url(self, *args, **kwargs) -> str:
        return faker.image_url()


@pytest.fixture
def database():
    return MockDatabase()


@pytest.fixture
def s3_client():
    return MockMinioClient()


@pytest.fixture
def get_all_birthdays(database, s3_client):
    return GetAllBirthdays(database, s3_client)


def test_get_all_birthdays_success(get_all_birthdays, database):
    args = MultiDict(
        [
            ("page", 1),
            ("per_page", 5),
        ]
    )

    with app.test_request_context(query_string=args):
        _, status_code = get_all_birthdays.execute()

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
