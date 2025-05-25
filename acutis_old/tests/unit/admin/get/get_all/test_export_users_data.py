from unittest.mock import MagicMock

import pytest
from faker import Faker

from handlers.admin.get.get_all.export_users_data import ExportUsersData
from main import app
from repositories.admin_repository import AdminRepository

faker = Faker("pt_BR")


class MockQuery:
    def __init__(self) -> None:
        self.join = MagicMock(return_value=self)
        self.filter = MagicMock(return_value=self)
        self.order_by = MagicMock(return_value=self)
        self.all = MagicMock(
            return_value=[
                MagicMock(
                    pais="brasil",
                    nome="Pedro Levi Moura",
                    nome_social="Pedro Moura",
                    numero_documento="49184051930",
                    email="pedro.levi.moura@cancaonova.com",
                    telefone="84986326434",
                    data_nascimento="01/07/1944",
                    sexo="masculino",
                    cep="59633619",
                    estado="SP",
                    cidade="São Paulo",
                    bairro="Santo Amaro",
                    rua="Rua 15",
                    numero="1556",
                    complemento="Bloco B",
                ),
                MagicMock(
                    pais="brasil",
                    nome="João Pedro Moura",
                    nome_social="João Moura",
                    numero_documento="49184051930",
                    email="joao.levi.moura@cancaonova.com",
                    telefone="84986326434",
                    data_nascimento="01/07/1944",
                    sexo="masculino",
                    cep="59633619",
                    estado="SP",
                    cidade="São Paulo",
                    bairro="Santo Amaro",
                    rua="Rua 15",
                    numero="1556",
                    complemento="Bloco B",
                ),
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
def export_excel():
    def mock_export_excel(*args, **kwargs):
        return {"url": faker.url()}

    return mock_export_excel


@pytest.fixture
def export_users_data(database, export_excel):
    admin_repository = AdminRepository(database)
    return ExportUsersData(admin_repository, export_excel)


def test_export_users_data(export_users_data, database):
    with app.test_request_context():
        _, status_code = export_users_data.execute()
        assert status_code == 200

        session_mock = database.session
        query_mock = session_mock.query

        query_mock.assert_called_once()

        join_mock = query_mock.return_value.join
        join_mock.assert_called()

        filter_mock = query_mock.return_value.filter
        filter_mock.assert_called_once()

        order_by_mock = query_mock.return_value.order_by
        order_by_mock.assert_called_once()

        all_mock = query_mock.return_value.all
        all_mock.assert_called_once()
