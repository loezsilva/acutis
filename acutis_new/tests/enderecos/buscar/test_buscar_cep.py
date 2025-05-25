from http import HTTPStatus

from flask.testing import FlaskClient


def test_buscar_cep_sucesso(client: FlaskClient):
    response = client.get('/api/enderecos/buscar-cep/60874-805')

    assert response.status_code == HTTPStatus.OK
    assert response.json == {
        'bairro': 'Pedras',
        'cep': '60874805',
        'cidade': 'Fortaleza',
        'estado': 'CE',
        'rua': 'Avenida Dionísio Alencar',
        'tipo_logradouro': 'Avenida',
    }


def test_buscar_cep_erro_cep_nao_encontrado(client: FlaskClient):
    response = client.get('/api/enderecos/buscar-cep/15975321')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json == [{'msg': 'CEP não encontrado na base de dados.'}]
