import json
from http import HTTPStatus

from flask.testing import FlaskClient

DELETAR_PROGRAMACAO_ENDPOINT = '/api/admin/lives/deletar-programacao-live'
JSON_CONTENT_TYPE = 'application/json'


def test_deletar_programacao_live_sucesso(
    client: FlaskClient, seed_registrar_live_avulsa, membro_token
):
    _, tipo_programacao = seed_registrar_live_avulsa

    payload = {
        'programacao_id': str(tipo_programacao.id),
        'tipo_programacao': 'avulsa',
    }

    response = client.delete(
        DELETAR_PROGRAMACAO_ENDPOINT,
        data=json.dumps(payload),
        content_type=JSON_CONTENT_TYPE,
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json == {
        'msg': 'Programação da live deletada com sucesso.'
    }


def test_deletar_programacao_live_nao_encontrada(
    client: FlaskClient, membro_token
):
    payload = {
        'programacao_id': '3fa85f64-5717-4562-b3fc-2c963f66afa6',
        'tipo_programacao': 'avulsa',
    }

    response = client.delete(
        DELETAR_PROGRAMACAO_ENDPOINT,
        data=json.dumps(payload),
        content_type=JSON_CONTENT_TYPE,
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json == [{'msg': 'Programação da live não encontrada.'}]
