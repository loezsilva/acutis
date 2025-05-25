

from http import HTTPStatus
from flask.testing import FlaskClient

def test_listar_recorrencias_canceladas_success(test_client: FlaskClient, seed_admin_user_token, seed_pedido_recorrente_cancelado):
    response = test_client.get(
        "/checkout/listar-recorrencias-canceladas",
        headers=seed_admin_user_token
    )
    
    assert response.status_code == HTTPStatus.OK
    data_response = response.get_json()
    
    assert "card_qtd_doacoes" in data_response and isinstance(data_response["card_qtd_doacoes"], int)
    assert "card_soma_valor_doacoes" in data_response  and isinstance(data_response["card_soma_valor_doacoes"], str)
    assert "doacoes_recorrentes_canceladas" in data_response  and isinstance(data_response["doacoes_recorrentes_canceladas"], list)
    