from http import HTTPStatus
from wsgiref import headers
from flask.testing import FlaskClient

def test_listar_todas_doacoes(test_client: FlaskClient, seed_admin_user_token):
    
    response = test_client.get(
        "checkout/listar-todas-doacoes",
        headers=seed_admin_user_token
    )
    
    assert response.status_code == HTTPStatus.OK
    