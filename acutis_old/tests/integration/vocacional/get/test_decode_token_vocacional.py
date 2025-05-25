from http import HTTPStatus
from flask.testing import FlaskClient

from utils.token_email import generate_token

def test_decode_token_vocacional_sucess(test_client: FlaskClient, seed_pre_cadastro_vocacional_pendentes):
    
    pre_cadastro, etapa = seed_pre_cadastro_vocacional_pendentes[0]
    
    payload_vocacional = {"fk_usuario_vocacional_id": pre_cadastro.id}
    token = generate_token(payload_vocacional, salt="decode-token-vocacional")
    
    response = test_client.get(
        f"/vocacional/decodificar-token-vocacional/{token}"
    )
    
    assert response.status_code == HTTPStatus.OK
    data_response = response.get_json()
       
    assert  isinstance(data_response, dict)
    assert "email" in data_response and isinstance(data_response["email"], str)
    assert "etapa" in data_response and isinstance(data_response["etapa"], str)
    assert "fk_usuario_vocacional_id" in data_response and isinstance(data_response["fk_usuario_vocacional_id"], int)
    assert "nome" in data_response and isinstance(data_response["nome"], str)
    assert "pais" in data_response and isinstance(data_response["pais"], str)
    assert "status" in data_response and isinstance(data_response["status"], str)
    assert "telefone" in data_response and isinstance(data_response["telefone"], str)
    
    
def test_decode_token_vocacional_vocacional_not_found(test_client: FlaskClient):
    
    payload_vocacional = {"fk_usuario_vocacional_id": 5252}
    token = generate_token(payload_vocacional, salt="decode-token-vocacional")
    
    response = test_client.get(
        f"/vocacional/decodificar-token-vocacional/{token}"
    )
    
    assert response.status_code == HTTPStatus.NOT_FOUND
    data_response = response.get_json()
       
    assert data_response["error"] == "Vocacional não encontrado."    
    