from unittest.mock import MagicMock
from faker import Faker
import pytest

from handlers.admin.get.get_by_id.get_action_details_by_id import GetActionDetailsById
from main import app


faker = Faker(locale="pt_BR")


class MockQuery:
    def __init__(self) -> None:
        self.outerjoin = MagicMock(return_value=self)
        self.join = MagicMock(return_value=self)
        self.filter = MagicMock(return_value=self)
        self.count = MagicMock(return_value=3)
        self.first = MagicMock(
            return_value=MagicMock(
                id=1,
                nome=faker.name(),
                titulo=faker.name(),
                descricao=faker.name(),
                background=faker.uuid4(),
                banner=faker.uuid4(),
                status=True,
                preenchimento_foto=True,
                label_foto=faker.name(),
                sorteio=True,
                criado_em=faker.date(),
                cadastrado_por=faker.name(),
            )
        )
        self.all = MagicMock(
            return_value=[
                MagicMock(
                    nome=faker.name(),
                    data_sorteio=faker.date(),
                    sorteador="John Doe",
                ),
                MagicMock(
                    nome=faker.name(),
                    data_sorteio=faker.date(),
                    sorteador="John Doe",
                ),
                MagicMock(
                    nome=faker.name(),
                    data_sorteio=faker.date(),
                    sorteador="John Doe",
                ),
            ]
        )


class MockSession:
    def __init__(self) -> None:
        self.query = MagicMock(return_value=MockQuery())


class MockDatabase:
    def __init__(self) -> None:
        self.session = MockSession()


class MockMinioClient:
    def get_public_url(self, *args, **kwargs) -> str:
        return faker.image_url()


@pytest.fixture
def s3_client():
    return MockMinioClient()


@pytest.fixture
def database():
    return MockDatabase()


@pytest.fixture
def get_action_details_by_id(database, s3_client):
    return GetActionDetailsById(database, s3_client)


def test_get_action_details_by_id_success(get_action_details_by_id, database):
    with app.test_request_context():
        _, status_code = get_action_details_by_id.execute(1)

        assert status_code == 200

        session_mock = database.session
        query_mock = session_mock.query

        query_mock.assert_called()

        filter_mock = query_mock.return_value.filter
        filter_mock.assert_called()

        first_mock = query_mock.return_value.first
        first_mock.assert_called_once()

        count_mock = query_mock.return_value.count
        count_mock.assert_called_once()

        all_mock = query_mock.return_value.all
        all_mock.assert_called_once()
