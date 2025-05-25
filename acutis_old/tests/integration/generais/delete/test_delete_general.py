from flask.testing import FlaskClient
from models.generais import Generais

def test_delete_general(test_client: FlaskClient, seed_admin_user_token, seed_general_not_aproved):
    
    user, clifor, address, _, general =  seed_general_not_aproved

    
    response = test_client.delete(
        f"/groups/delete-general/{general.id}",
        headers=seed_admin_user_token
    )
    
    verify_deletion = Generais.query.filter_by(id=general.id).first()
    
    assert response.status_code == 200
    assert response.json["msg"] == "General deletado com sucesso."
    assert verify_deletion.deleted_at is not None
    
    