from unittest.mock import MagicMock

from faker import Faker
from werkzeug.datastructures import MultiDict
import pytest

from handlers.admin.get.get_all.get_all_leads import GetAllLeads
from main import app
from utils.functions import get_current_time

faker = Faker()


class MockQuery:
    def __init__(self) -> None:
        self.items = [
            MagicMock(
                id=1,
                nome=faker.name(),
                email=faker.email(),
                telefone=faker.phone_number(),
                origem="campanha 1",
                data_final=get_current_time().strftime("%d/%m/%Y %H:%M:%S"),
                data_download=None,
                sorteado=True,
                download_usuario_id=None,
                intencao="Intenção boa",
            ),
            MagicMock(
                id=2,
                nome=faker.name(),
                email=faker.email(),
                telefone=faker.phone_number(),
                origem="campanha 2",
                data_final=get_current_time().strftime("%d/%m/%Y %H:%M:%S"),
                data_download=None,
                sorteado=True,
                download_usuario_id=None,
                intencao="Intenção muito boa",
            ),
        ]
        self.total = 2
        self.join = MagicMock(return_value=self)
        self.filter = MagicMock(return_value=self)
        self.order_by = MagicMock(return_value=self)
        self.outerjoin = MagicMock(return_value=self)
        self.all = MagicMock(return_value=[])
        self.paginate = MagicMock(
            return_value=MagicMock(items=self.items, total=self.total)
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
def get_all_leads(database, s3_client):
    return GetAllLeads(database, s3_client)


def test_get_all_leads_success(get_all_leads, database):
    args = MultiDict(
        [
            ("page", 1),
            ("per_page", 5),
        ]
    )

    with app.test_request_context(query_string=args):
        _, status_code = get_all_leads.execute()

        assert status_code == 200

        session_mock = database.session
        query_mock = session_mock.query

        query_mock.assert_called()

        filter_mock = query_mock.return_value.filter
        filter_mock.assert_called_once()

        order_by_mock = query_mock.return_value.order_by
        order_by_mock.assert_called_once()

        paginate_mock = query_mock.return_value.paginate
        paginate_mock.assert_called_once()

        outerjoin_mock = query_mock.return_value.outerjoin
        outerjoin_mock.assert_called()

        all_mock = query_mock.return_value.all
        all_mock.assert_called_once()
