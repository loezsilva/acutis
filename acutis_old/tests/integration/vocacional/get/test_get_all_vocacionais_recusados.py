from http import HTTPStatus
from flask.testing import FlaskClient

def test_get_vocacionais_recusados(test_client: FlaskClient, seed_admin_user_token, seed_vocacionais_reprovados):
    
    response = test_client.get(
        "/vocacional/listar-vocacionais-recusados?",
        headers=seed_admin_user_token
    )
    
    assert response.status_code == HTTPStatus.OK
    data_response = response.get_json()
    
    assert "recusados" in data_response and isinstance(data_response["recusados"], list)
    assert "page" in data_response and isinstance(data_response["page"], int)
    assert "total" in data_response and isinstance(data_response["total"], int)
    
    assert isinstance(data_response["page"], int)
    assert isinstance(data_response["total"], int)
    assert isinstance(data_response["recusados"], list)
         