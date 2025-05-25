from flask.testing import FlaskClient
from http import HTTPStatus
import json

def test_get_campaigns_publics_success(test_client: FlaskClient):
    response = test_client.get("/campaigns/campanhas-publicas")
    assert response.status_code == HTTPStatus.OK
    
    data = response.get_json()
    if data != None:
        assert "campanhas" in data
        assert "page" in data
        assert "total" in data
        
        assert isinstance(data["campanhas"], list)

        for campanha in data["campanhas"]:
            assert "descricao" in campanha
            assert "id" in campanha
            assert "imagem_campanha" in campanha
            assert "objetivo" in campanha
            assert "titulo" in campanha

            assert isinstance(campanha["descricao"], str)
            assert isinstance(campanha["id"], int)
            assert isinstance(campanha["imagem_campanha"], str)
            assert isinstance(campanha["objetivo"], str)
            assert isinstance(campanha["titulo"], str)
        
        
def test_get_campaigns_publics_by_id_success(test_client: FlaskClient ):
    
    response = test_client.get("/campaigns/campanhas-publicas")
    assert response.status_code == HTTPStatus.OK
    
    data = response.get_json()
    
    if data != None:
        for campanha in data["campanhas"]:
            
            response = test_client.get(f"/campaigns/campanhas-publicas/{campanha['id']}")
            assert response.status_code == HTTPStatus.OK
            
            data = response.get_json()
            
            assert "descricao" in data
            assert "id" in data
            assert "imagem_campanha" in data
            assert "objetivo" in data
            assert "titulo" in data

            assert data["status"] == True
            assert data["publica"] == True

            assert isinstance(data["descricao"], str)
            assert isinstance(data["id"], int)
            assert isinstance(data["imagem_campanha"], str)
            assert isinstance(data["objetivo"], str)
            assert isinstance(data["titulo"], str)