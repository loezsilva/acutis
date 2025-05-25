from flask.testing import FlaskClient


def test_promove_general_to_marechal(
    test_client: FlaskClient, seed_general_not_aproved, seed_admin_user_token
):

    _, _, _, _, general = seed_general_not_aproved

    # aprova general reutilizando seed de general nao aprovado
    # isso é necessário para que o general possa ser promovido
    # reutilizando seed de general nao aprovado

    test_client.put(
        f"/groups/alter-status-general/{general.id}",
        headers=seed_admin_user_token,
    )

    assert general.status == True

    response = test_client.put(
        f"/groups/alter-cargo-general/{general.id}", 
        json={"acao": "promover"},
        headers=seed_admin_user_token,
    )
        
    assert response.status_code == 200
    data = response.get_json()
    assert data["msg"] == "General promovido a marechal com sucesso!"
