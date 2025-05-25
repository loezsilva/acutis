from http import HTTPStatus

from flask.testing import FlaskClient

from acutis_api.application.utils.funcoes_auxiliares import gerar_token
from acutis_api.communication.responses.vocacional import (
    DecodificarTokenVocacionalResponse,
)


def test_decodifica_token_vocacional_sucesso(
    client: FlaskClient, seed_pre_cadastro_vocacional_pendentes
):
    pre_cadastro, _ = seed_pre_cadastro_vocacional_pendentes[0]

    payload_vocacional = {'fk_usuario_vocacional_id': str(pre_cadastro.id)}
    token = gerar_token(payload_vocacional, salt='decode-token-vocacional')

    response = client.get(
        f'/api/vocacional/decodificar-token-vocacional/{token}'
    )

    assert response.status_code == HTTPStatus.OK
    data_response = response.get_json()

    assert DecodificarTokenVocacionalResponse.model_validate(data_response)


def test_decodifica_token_vocacional_nao_encontrado(client: FlaskClient):
    payload_vocacional = {
        'fk_usuario_vocacional_id': '0C8C99E4-62A7-4D55-A793-0E6244E3ECB2'
    }
    token = gerar_token(payload_vocacional, salt='decode-token-vocacional')

    response = client.get(
        f'/api/vocacional/decodificar-token-vocacional/{token}'
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    data_response = response.get_json()

    assert data_response == [{'msg': 'Vocacional não encontrado.'}]
