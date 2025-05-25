from unittest.mock import MagicMock
from faker import Faker
import pytest

from handlers.users.get.get_by_id.get_cpf_registration_status import (
    GetCpfRegistrationStatus,
)
from main import app

faker = Faker()


class MockQuery:
    def __init__(self, user_exists=True) -> None:
        self.first = MagicMock(
            return_value=(
                MagicMock(
                    nome=faker.name(),
                    nome_social=faker.name(),
                    obriga_atualizar_cadastro=True,
                    obriga_atualizar_endereco=False,
                )
                if user_exists
                else None
            )
        )
        self.select_from = MagicMock(return_value=self)
        self.join = MagicMock(return_value=self)
        self.filter = MagicMock(return_value=self)


class MockSession:
    def __init__(self, user_exists=True) -> None:
        self.query = MagicMock(return_value=MockQuery(user_exists=user_exists))


class MockDatabase:
    def __init__(self, user_exists=True) -> None:
        self.session = MockSession(user_exists=user_exists)


@pytest.fixture
def database():
    return MockDatabase()


@pytest.fixture
def handler(database):
    return GetCpfRegistrationStatus(database)


def test_get_cpf_registration_status_success(handler, database):
    with app.test_request_context(
        query_string={"numero_documento": "78567639069", "tipo_documento": "cpf"}
    ):
        response, status_code = handler.execute()

        assert status_code == 200
        assert response["possui_conta"] is True
        assert response["atualizar_conta"] is True

        session_mock = database.session
        query_mock = session_mock.query

        query_mock.assert_called_once()

        select_from_mock = query_mock.return_value.select_from
        select_from_mock.assert_called_once()

        join_mock = query_mock.return_value.join
        join_mock.assert_called()

        filter_mock = query_mock.return_value.filter
        filter_mock.assert_called_once()

        first_mock = query_mock.return_value.first
        first_mock.assert_called_once()


def test_get_cpf_registration_status_user_not_found(handler, database):
    database_no_user = MockDatabase(user_exists=False)
    handler_no_user = GetCpfRegistrationStatus(database_no_user)

    with app.test_request_context(
        query_string={"numero_documento": "78567639069", "tipo_documento": "cpf"}
    ):
        response, status_code = handler_no_user.execute()

        assert status_code == 200
        assert response["possui_conta"] is False
        assert response["atualizar_conta"] is False

        session_mock = database_no_user.session
        query_mock = session_mock.query

        query_mock.assert_called_once()

        select_from_mock = query_mock.return_value.select_from
        select_from_mock.assert_called_once()

        join_mock = query_mock.return_value.join
        join_mock.assert_called()

        filter_mock = query_mock.return_value.filter
        filter_mock.assert_called_once()

        first_mock = query_mock.return_value.first
        first_mock.assert_called_once()
