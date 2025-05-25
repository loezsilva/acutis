from unittest.mock import MagicMock
from faker import Faker
import pytest
from handlers.admin.get.get_all.get_all_users_presences import GetAllUsersPresences
from werkzeug.datastructures import MultiDict
from main import app

faker = Faker("pt_BR")


class MockQuery:
    def __init__(self):
        self.select_from = MagicMock(return_value=self)
        self.join = MagicMock(return_value=self)
        self.outerjoin = MagicMock(return_value=self)
        self.filter = MagicMock(return_value=self)
        self.order_by = MagicMock(return_value=self)
        self.paginate = MagicMock(
            return_value=MagicMock(
                items=[
                    MagicMock(
                        id=1,
                        nome=faker.name(),
                        email=faker.email(),
                        numero_documento="1541654161521",
                        presencas=77,
                        foto="test_photo.jpg",
                        fk_campanha_id=1,
                        nome_campanha=faker.name(),
                    ),
                    MagicMock(
                        id=2,
                        nome=faker.name(),
                        email=faker.email(),
                        numero_documento="8954216451516",
                        presencas=25,
                        foto="test2_photo.jpg",
                        fk_campanha_id=1,
                        nome_campanha=faker.name(),
                    ),
                ],
                total=2,
            )
        )


class MockSession:
    def __init__(self):
        self.query = MagicMock(return_value=MockQuery())


class MockDatabase:
    def __init__(self):
        self.session = MockSession()


class MockMinIOClient:
    def get_public_url(self, *args, **kwargs):
        return faker.image_url()


@pytest.fixture
def minio_client():
    return MockMinIOClient()


@pytest.fixture
def database():
    return MockDatabase()


@pytest.fixture
def get_all_users_presences(database, minio_client):
    return GetAllUsersPresences(database, minio_client)


def test_get_all_users_presences_success(get_all_users_presences, database):
    args = MultiDict(
        [
            ("page", 1),
            ("per_page", 5),
        ]
    )

    with app.test_request_context(query_string=args):
        _, status_code = get_all_users_presences.execute()

        assert status_code == 200

        session_mock = database.session
        query_mock = session_mock.query

        query_mock.assert_called_once()

        select_from_mock = query_mock.return_value.select_from
        select_from_mock.assert_called_once()

        join_mock = query_mock.return_value.join
        join_mock.assert_called()

        outerjoin_mock = query_mock.return_value.outerjoin
        outerjoin_mock.assert_called_once()

        filter_mock = query_mock.return_value.filter
        filter_mock.assert_called_once()

        order_by_mock = query_mock.return_value.order_by
        order_by_mock.assert_called_once()

        paginate_mock = query_mock.return_value.paginate
        paginate_mock.assert_called_once()
