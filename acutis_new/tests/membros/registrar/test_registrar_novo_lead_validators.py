import uuid
from http import HTTPStatus

from flask.testing import FlaskClient


def test_erro_nome_com_caracteres_invalidos(client: FlaskClient):
    payload = {
        'nome': 'Yan P1st0l3ir0',
        'email': 'emailtest@gmail.com',
        'telefone': '85998685421',
        'pais': 'brasil',
        'campanha_id': str(uuid.uuid4()),
        'origem_cadastro': 'acutis',
    }

    response = client.post('/api/membros/registrar-novo-lead', json=payload)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json[0]['msg'] == (
        'O nome Yan P1st0l3ir0 possui caracteres inválidos.'
    )


def test_erro_nome_com_mais_de_100_caracteres(client: FlaskClient):
    payload = {
        'nome': 'MaximilianoSebastianoFilipeRodriguezAntonioFernandezGuillermoAlexandreTheodoroCristobalVasquezDominguezHernandez',  # noqa
        'email': 'emailtest@gmail.com',
        'telefone': '85998685421',
        'pais': 'brasil',
        'campanha_id': str(uuid.uuid4()),
        'origem_cadastro': 'acutis',
    }

    response = client.post('/api/membros/registrar-novo-lead', json=payload)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json[0]['msg'] == (
        'O nome deve conter no máximo 100 caracteres.'
    )
