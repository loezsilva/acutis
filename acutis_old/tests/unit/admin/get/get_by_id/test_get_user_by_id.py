from unittest.mock import MagicMock

from faker import Faker
import pytest

from handlers.admin.get.get_by_id.get_user_by_id import GetUserById
from main import app


faker = Faker(locale="pt_BR")


class MockQuery:
    def __init__(self):
        self.select_from = MagicMock(return_value=self)
        self.join = MagicMock(return_value=self)
        self.filter = MagicMock(return_value=self)
        self.first = MagicMock(
            return_value=MagicMock(
                id=1,
                nome=faker.name(),
                nome_social=faker.name(),
                email=faker.email(),
                pais=faker.country(),
                origem_cadastro="campanha 1",
                status=True,
                data_cadastro=faker.date(),
                ultimo_acesso=faker.date(),
                avatar=faker.image_url(),
                numero_documento=faker.cpf(),
                telefone=faker.phone_number(),
                perfil="Benfeitor",
            )
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


class FileServiceMock:
    def get_public_url(self, *args, **kwargs) -> str:
        return faker.image_url()


@pytest.fixture
def file_service():
    return FileServiceMock()


@pytest.fixture
def get_user_by_id(database, file_service):
    return GetUserById(database, file_service)


def test_get_user_by_id_success(get_user_by_id, database):
    with app.test_request_context():
        _, status_code = get_user_by_id.execute(1)

        assert status_code == 200

        session_mock = database.session
        query_mock = session_mock.query

        query_mock.assert_called_once()

        filter_mock = query_mock.return_value.filter
        filter_mock.assert_called_once()

        first_mock = query_mock.return_value.first
        first_mock.assert_called_once()
