from http import HTTPStatus
from flask.testing import FlaskClient
from models.generais import Generais

def test_aprove_general(
    test_client: FlaskClient, seed_general_not_aproved, seed_admin_user_token
):
    
    _, _, _, _, general =  seed_general_not_aproved
    
    response = test_client.put(
        f"/groups/alter-status-general/{general.id}",
        headers=seed_admin_user_token,
    )
    
    assert response.status_code == HTTPStatus.OK  
    general_after_aproved = Generais.query.get(general.id)    
    assert general_after_aproved.status == True
    
    data_response = response.get_json()
    assert data_response["msg"] == "general aprovado com sucesso!"
    
