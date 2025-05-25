from http import HTTPStatus
from re import A
from flask.testing import FlaskClient


def test_desistencia_usuario_vocacional_sucess(
    test_client: FlaskClient, seed_pre_cadastro_vocacional_pendentes
):

    vocacional = seed_pre_cadastro_vocacional_pendentes[0][0]

    vocacional_id = vocacional.id

    response = test_client.post(f"/vocacional/registrar-desistencia/{vocacional_id}", json={})

    assert response.status_code == HTTPStatus.OK
    data = response.get_json()
    assert data["msg"] == "Sua desistência foi registrada com sucesso."


def test_desistencia_usuario_vocacional_com_conflito(
    test_client: FlaskClient, seed_pre_cadastro_vocacional_desistencia
):
    vocacional, etapa = seed_pre_cadastro_vocacional_desistencia

    vocacional_id = vocacional.id
    
    response_conflict = test_client.post(
        f"/vocacional/registrar-desistencia/{vocacional_id}", json={}
    )

    assert response_conflict.status_code == HTTPStatus.CONFLICT
    data_conflict = response_conflict.get_json()
    assert data_conflict["error"] == "Desistência já realizada anteriormente."
       