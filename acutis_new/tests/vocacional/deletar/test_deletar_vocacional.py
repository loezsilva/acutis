from http import HTTPStatus

from flask.testing import FlaskClient


def test_delete_vocacional(
    client: FlaskClient,
    membro_token,
    seed_pre_cadastro_vocacional_pendentes,
):
    pre_cadastro, _ = seed_pre_cadastro_vocacional_pendentes[0]

    response = client.delete(
        f'/api/vocacional/deletar-vocacional/{str(pre_cadastro.id)}',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    data_response = response.get_json()
    assert data_response == {'msg': 'Usuário vocacional deletado com sucesso.'}


def test_delete_vocacional_nao_encontrado(
    client: FlaskClient,
    membro_token,
):
    response = client.delete(
        '/api/vocacional/deletar-vocacional/0C8C99E4-62A7-4D55-A793-0E6244E3ECB2',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    data_response = response.get_json()
    assert data_response == [{'msg': 'Vocacional não encontrado.'}]
