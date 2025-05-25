from http import HTTPStatus
from flask.testing import FlaskClient


def test_reprova_vocacional(
    test_client: FlaskClient,
    seed_pre_cadastro_vocacional_pendentes,
    seed_admin_user_token,
):

    registro = seed_pre_cadastro_vocacional_pendentes[0][0]

    vocacional_id = registro.id

    response = test_client.put(
        "/vocacional/atualizar-andamento-vocacional",
        headers=seed_admin_user_token,
        json={"acao": "reprovar", "usuario_vocacional_id": vocacional_id},
    )

    assert response.status_code == HTTPStatus.OK
    data = response.get_json()
    assert data["msg"] == "Vocacional reprovado com sucesso."

    
def test_reprova_vocacional_conflito(
    test_client: FlaskClient,
    seed_pre_cadastro_vocacional_reproved,
    seed_admin_user_token,
):

    registro, etapa = seed_pre_cadastro_vocacional_reproved

    vocacional_id = registro.id

    response_conflict = test_client.put(
        "/vocacional/atualizar-andamento-vocacional",
        headers=seed_admin_user_token,
        json={"acao": "reprovar", "usuario_vocacional_id": vocacional_id},
    )

    assert response_conflict.status_code == HTTPStatus.CONFLICT
    data_conflict = response_conflict.get_json()
    assert data_conflict["error"] == "Vocacional já reprovado anteriormente."
