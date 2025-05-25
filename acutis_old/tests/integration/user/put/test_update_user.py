import io
import json
from flask.testing import FlaskClient
from flask_jwt_extended import create_access_token
from builder import db


def test_update_user_success(
    test_client: FlaskClient, seed_user_with_dependencies
):

    user, clifor, address, _ = seed_user_with_dependencies

    avatar = (io.BytesIO(b"fake_image_data"), "avatar.jpg")

    payload = {
        "data": json.dumps(
            {
                "usuario": {
                    "nome": "Martin Ford",
                    "nome_social": "M Ford",
                    "data_nascimento": "1983-02-04",
                    "telefone": "(85) 98682-5573",
                    "sexo": "masculino",
                },
                "endereco": {
                    "cep": "44096584",
                    "rua": "Rua das Angélicas",
                    "numero": "8965",
                    "bairro": "Aviário",
                    "estado": "BA",
                    "cidade": "Feira de Santana",
                },
            }
        )
    }

    access_token = create_access_token(identity=user.id)

    response = test_client.put(
        "/users/update",
        data={
            **payload,
            "image": avatar,
        },
        content_type="multipart/form-data",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["msg"] == "Usuário atualizado com sucesso."

    db.session.refresh(user)
    assert user.nome == "Martin Ford"
    assert user.nome_social == "M Ford"

    db.session.refresh(clifor)
    assert clifor.data_nascimento.strftime("%Y-%m-%d") == "1983-02-04"

    db.session.refresh(address)
    assert address.cep == "44096584"
    assert address.rua == "Rua das Angélicas"
    assert address.numero == "8965"
    assert address.bairro == "Aviário"
    assert address.estado == "BA"
    assert address.cidade == "Feira de Santana"
