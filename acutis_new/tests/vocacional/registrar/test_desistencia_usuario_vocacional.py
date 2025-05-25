from http import HTTPStatus

from flask.testing import FlaskClient

from tests.factories import UsuarioVocacionalFactory


def test_desistencia_usuario_vocacional_sucesso(
    client: FlaskClient, seed_pre_cadastro_vocacional_pendentes
):
    vocacional = seed_pre_cadastro_vocacional_pendentes[0][0]

    vocacional_id = vocacional.id

    response = client.post(
        f'/api/vocacional/registrar-desistencia/{vocacional_id}', json={}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.get_json() == {
        'msg': 'Sua desistência foi registrada com sucesso.'
    }


def test_desistencia_usuario_vocacional_com_conflito(
    client: FlaskClient, seed_pre_cadastro_vocacional_desistencia
):
    vocacional, _ = seed_pre_cadastro_vocacional_desistencia()

    vocacional_id = vocacional.id

    response_conflict = client.post(
        f'/api/vocacional/registrar-desistencia/{vocacional_id}', json={}
    )

    assert response_conflict.status_code == HTTPStatus.CONFLICT
    assert response_conflict.get_json() == [
        {'msg': 'Desistência já realizada anteriormente.'}
    ]


def test_desistencia_usuario_vocacional_inexistente(client: FlaskClient):
    usuario_vocacional = UsuarioVocacionalFactory()
    vocacional_id = usuario_vocacional.id

    response = client.post(
        f'/api/vocacional/registrar-desistencia/{vocacional_id}', json={}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.get_json() == [{'msg': 'Etapa vocacional não encontrada.'}]
