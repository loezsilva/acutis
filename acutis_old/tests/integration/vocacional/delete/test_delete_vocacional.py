from http import HTTPStatus
from flask.testing import FlaskClient

def test_delete_vocacional(
    test_client: FlaskClient,
    seed_admin_user_token,
    seed_pre_cadastro_vocacional_pendentes,
):

    pre_cadastro, etapa = seed_pre_cadastro_vocacional_pendentes[0]

    response = test_client.delete(
        f"/vocacional/deletar-vocacional/{pre_cadastro.id}",
        headers=seed_admin_user_token,
    )

    assert response.status_code == HTTPStatus.OK
    data_response = response.get_json()
    assert data_response["msg"] == "Usuário vocacional deletado com sucesso."
