from http import HTTPStatus
from flask.testing import FlaskClient


def test_listar_pre_cadastros_vocacionais(
    test_client: FlaskClient,
    seed_admin_user_token,
    seed_pre_cadastro_vocacional_pendentes,
):

    response = test_client.get(
        "/vocacional/listar-pre-cadastros", headers=seed_admin_user_token
    )

    assert response.status_code == HTTPStatus.OK

    data = response.get_json()
    
    assert "page" in data and isinstance(data["page"], int)
    assert "total" in data and isinstance(data["total"], int)
    assert "pre_cadastros" in data and isinstance(data["pre_cadastros"], list)
