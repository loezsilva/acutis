from flask.testing import FlaskClient
from builder import db


def test_update_address_by_user_id_success(
    test_client: FlaskClient,
    seed_admin_user_token,
    seed_user_to_test_edit_address,
):
    user, address = seed_user_to_test_edit_address

    payload = {
        "cep": "65608605",
        "rua": "Travessa São José",
        "numero": "7745",
        "bairro": "Fazendinha",
        "cidade": "Caxias",
        "estado": "MA",
    }

    response = test_client.put(
        f"/administradores/editar-endereco-usuario/{user.id}",
        json=payload,
        headers=seed_admin_user_token,
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["msg"] == "Endereço atualizado com sucesso"

    db.session.refresh(address)
    assert address.cep == "65608605"
    assert address.rua == "Travessa São José"
    assert address.numero == "7745"
    assert address.bairro == "Fazendinha"
    assert address.cidade == "Caxias"
    assert address.estado == "MA"
