from unittest.mock import MagicMock
from faker import Faker
import pytest

from handlers.admin.get.get_by_id.get_address_by_user_id import GetAddressByUserId
from main import app
from models.endereco import Endereco
from models.usuario import Usuario

faker = Faker(locale="pt_BR")


class MockQuery:
    def __init__(self) -> None:
        self.select_from = MagicMock(return_value=self)
        self.join = MagicMock(return_value=self)
        self.filter = MagicMock(return_value=self)
        self.first = MagicMock(
            return_value=MagicMock(
                id=1,
                cep=faker.postcode(),
                rua=faker.street_name(),
                numero=faker.building_number(),
                complemento="Próximo ao shopping",
                bairro=faker.neighborhood(),
                cidade=faker.city(),
                estado=faker.state(),
                pais_origem=faker.country(),
                detalhe_estrangeiro=None,
            )
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
def get_address_by_user_id(database):
    return GetAddressByUserId(database)


def test_get_address_by_user_id_success(get_address_by_user_id, database):
    with app.test_request_context():
        _, status_code = get_address_by_user_id.execute(1)

        assert status_code == 200

        session_mock = database.session
        query_mock = session_mock.query

        query_mock.assert_called_once_with(Endereco)

        select_from_mock = query_mock.return_value.select_from
        select_from_mock.assert_called_once_with(Usuario)

        join_mock = query_mock.return_value.join
        join_mock.assert_called()

        filter_mock = query_mock.return_value.filter
        filter_mock.assert_called_once()

        first_mock = query_mock.return_value.first
        first_mock.assert_called_once()
