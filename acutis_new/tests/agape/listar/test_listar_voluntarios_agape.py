from http import HTTPStatus
from flask.testing import FlaskClient

LISTAR_VOLUNTARIOS_ENDPOINT = 'api/agape/listar-voluntarios-agape'

def test_listar_voluntarios_agape_sucesso(
    client: FlaskClient, 
    seed_lead_voluntario_e_token
):
    
    token = seed_lead_voluntario_e_token[1]

    resposta = client.get(
        LISTAR_VOLUNTARIOS_ENDPOINT,
        headers={'Authorization': f'Bearer {token}'},
    )

    assert resposta.status_code == HTTPStatus.OK

    resposta_json = resposta.json

    assert 'resultados' in resposta_json
    assert 'total' in resposta_json
    assert 'pagina' in resposta_json
    assert 'paginas' in resposta_json

    assert isinstance(resposta_json['resultados'], list)
    assert len(resposta_json['resultados']) >= 1

    for voluntario in resposta_json['resultados']:
        assert 'id' in voluntario
        assert 'nome' in voluntario
        assert 'email' in voluntario


def test_listar_voluntarios_agape_sem_permissao(client: FlaskClient):
    
    resposta = client.get(LISTAR_VOLUNTARIOS_ENDPOINT)

    assert resposta.status_code == HTTPStatus.UNAUTHORIZED
