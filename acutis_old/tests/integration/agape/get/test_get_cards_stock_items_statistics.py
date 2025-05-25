from http import HTTPStatus
from flask.testing import FlaskClient

from utils.functions import get_current_time


def test_get_cards_stock_items_statistics(
    test_client: FlaskClient, seed_admin_user_token, seed_stock_statistics
) -> None:
    response = test_client.get(
        "/agape/cards-estatisticas-itens-estoque",
        headers=seed_admin_user_token,
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json["itens_em_estoque"] == "100 | Em estoque"
    assert (
        response.json["ultima_acao"]
        == f'{get_current_time().date().strftime("%d/%m/%Y")} | 100 Itens'
    )
    assert (
        response.json["ultima_entrada"]
        == f'{get_current_time().date().strftime("%d/%m/%Y")} | 10 Itens'
    )
