from flask.testing import FlaskClient
from models.generais import Generais
from http import HTTPStatus

def test_lower_marechal_to_general(test_client: FlaskClient, seed_admin_user_token, seed_marechal, seed_general_link_to_marechal) -> None:
    
    _, _, _, _, marechal = seed_marechal
        
    for general in seed_general_link_to_marechal:
        _, _, _, _, general_link_marechal = general
        assert general_link_marechal.fk_usuario_superior_id == marechal.id
    
    response = test_client.put(
        f"/groups/alter-cargo-general/{marechal.id}",
        headers=seed_admin_user_token,
        json={"acao": "rebaixar"}
    )
        
    assert response.status_code == HTTPStatus.OK
    assert marechal.fk_cargo_id == 2
    
    for general in seed_general_link_to_marechal:
        *_, general_link_marechal = general
        assert general_link_marechal.fk_usuario_superior_id == None
    