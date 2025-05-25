from http import HTTPStatus
from wsgiref import headers
from flask.testing import FlaskClient

def test_listar_cadastros_vocacionais(test_client: FlaskClient, seed_admin_user_token, seed_cadastro_vocacional_aprovado):
    
    
    response = test_client.get(
        "/vocacional/listar-cadastros-vocacionais",
        headers=seed_admin_user_token
    )

    assert response.status_code == HTTPStatus.OK
    
    data_response = response.get_json()

    assert "cadastros_vocacionais" in data_response
    assert "total" in data_response
    assert "page" in data_response

    assert isinstance(data_response["total"], int)
    assert isinstance(data_response["page"], int)
    assert isinstance(data_response["cadastros_vocacionais"], list)

