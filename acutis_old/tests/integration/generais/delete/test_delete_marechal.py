from flask.testing import FlaskClient
from models.generais import Generais
from http import HTTPStatus

def test_delete_marechal(test_client: FlaskClient, seed_admin_user_token, seed_marechal, seed_general_link_to_marechal ) -> None:
    
    _, _, _, _, marechal = seed_marechal
        
    for general in seed_general_link_to_marechal:
        _, _, _, _, general_link_marechal = general
        assert general_link_marechal.fk_usuario_superior_id == marechal.id
    
    response = test_client.delete(
        f"/groups/delete-general/{marechal.id}",
        headers=seed_admin_user_token
    )
        
    assert marechal.deleted_at is not None
    assert marechal.fk_cargo_id == 1

    assert general_link_marechal.fk_usuario_superior_id == None
    
    for general in seed_general_link_to_marechal:
        _, _, _, _, general_link_marechal = general
        assert general_link_marechal.fk_usuario_superior_id == None
    
    assert response.status_code == HTTPStatus.OK