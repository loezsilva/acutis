from http import HTTPStatus
from flask.testing import FlaskClient
from models.generais import Generais

def test_link_general_to_marechal(
    test_client: FlaskClient, seed_admin_user_token, seed_marechal, seed_general_not_aproved
):

    _, _, _, _, marechal = seed_marechal
    _, _, _, _, general = seed_general_not_aproved

    # aprova general reutilizando seed de general nao aprovado
    # isso é necessário para que o general possa ser promovido
    # reutilizando seed de general nao aprovado

    aprove = test_client.put(
        f"/groups/alter-status-general/{general.id}",
        headers=seed_admin_user_token,
    )
    
    assert aprove.status_code

    assert general.status == True

    response = test_client.put(
        f"/groups/alter-cargo-general/{general.id}", 
        json={"acao": "vincular", "marechal_id": marechal.id},
        headers=seed_admin_user_token,
    )
        
    assert response.status_code == HTTPStatus.OK
    
    general = Generais.query.get(general.id)
    assert general.fk_cargo_id == 2
    assert general.fk_usuario_superior_id == marechal.id
    
    data = response.get_json()
    assert data["msg"] == "General vinculado a Marechal com sucesso"
