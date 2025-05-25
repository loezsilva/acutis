from http import HTTPStatus
from flask.testing import FlaskClient


def test_get_desistencias_vocacionais(
    test_client: FlaskClient,
    seed_admin_user_token,
    seed_pre_cadastro_vocacional_desistencia,
):
    response = test_client.get(
        "/vocacional/listar-desistencias-vocacionais", headers=seed_admin_user_token
    )

    assert response.status_code == HTTPStatus.OK
    data_response = response.get_json()

    assert "desistencias" in data_response and isinstance(
        data_response["desistencias"], list
    )
    assert "page" in data_response and isinstance(data_response["page"], int)
    assert "total" in data_response and isinstance(data_response["total"], int)

