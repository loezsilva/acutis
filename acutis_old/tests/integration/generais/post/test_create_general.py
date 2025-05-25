from flask.testing import FlaskClient
from faker import Faker
from http import HTTPStatus

def test_create_general_success(test_client: FlaskClient, seed_user_with_dependencies):
    faker = Faker()
    
    user, _, _, _ = seed_user_with_dependencies
    
    data = {
        "fk_usuario_id": user.id,
        "quant_membros_grupo": 45,
        "nome_grupo": faker.name(),
        "link_grupo": "https://chat.whatsapp.com/bondade412312312312589",
        "tempo_de_administrador": 12
    }
    
    response = test_client.post(
        "/groups/registrar-general",
        json=data
    )
    
    assert response.status_code == HTTPStatus.CREATED
    assert response.json["msg"] == "General criado com sucesso!"
    

def test_create_general_user_not_found(test_client: FlaskClient):
    faker = Faker()
    
    data = {
        "fk_usuario_id": 999999,  # ID de um usuário que não existe
        "quant_membros_grupo": 45,
        "nome_grupo": faker.name(),
        "link_grupo": "https://chat.whatsapp.com/bondade412312312312589",
        "tempo_de_administrador": 12
    }
    
    response = test_client.post(
        "/groups/registrar-general",
        json=data
    )
    
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert "Usuário não encontrado." in response.json["error"]
    

def test_create_general_invalid_data(test_client: FlaskClient, seed_user_with_dependencies):
    faker = Faker()
    
    user, _, _, _ = seed_user_with_dependencies
    
    data = {
        "fk_usuario_id": user.id,
        "quant_membros_grupo": 45,
        "nome_grupo": faker.name(),
        "link_grupo": "https://chat.whatsapp.com/bondade",  # Link inválido 
        "tempo_de_administrador": 12
    }
    
    response = test_client.post(
        "/groups/registrar-general",
        json=data
    )
    
    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    
    
def test_create_general_already_exists(test_client: FlaskClient, seed_user_with_dependencies):
    faker = Faker()
    
    user, _, _, _ = seed_user_with_dependencies
    
    data = {
        "fk_usuario_id": user.id,
        "quant_membros_grupo": 45,
        "nome_grupo": faker.name(),
        "link_grupo": "https://chat.whatsapp.com/bondade412312312312589",
        "tempo_de_administrador": 12
    }
    
    response1 = test_client.post(
        "/groups/registrar-general",
        json=data
    )
    
    assert response1.status_code == HTTPStatus.CREATED
    
    response2 = test_client.post(
        "/groups/registrar-general",
        json=data
    )
    
    assert response2.status_code == HTTPStatus.CONFLICT
    assert response2.json["error"] == "General já cadastrado."