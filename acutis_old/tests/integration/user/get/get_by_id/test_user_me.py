from flask.testing import FlaskClient
from flask_jwt_extended import create_access_token


def test_user_me_success(test_client: FlaskClient, seed_user_with_dependencies):
    user, clifor, _, _ = seed_user_with_dependencies

    token = create_access_token(identity=user.id)

    response = test_client.get(
        "/users/me", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == user.id
    assert data["nome"] == user.nome
    assert data["email"] == user.email
    assert data["pais"] == user.country
    assert data["nome_social"] == user.nome_social
    assert data["numero_documento"] == clifor.cpf_cnpj
    assert data["data_nascimento"] == clifor.data_nascimento.strftime("%d/%m/%Y")
    assert data["telefone"] == clifor.telefone1
    assert data["sexo"] == clifor.sexo
