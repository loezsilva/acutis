import uuid
from http import HTTPStatus

from flask.testing import FlaskClient

ROTA = '/api/rotas-publicas/busca-cargo-superior'


def test_busca_cargo_superior_oficiais_not_found(client: FlaskClient):
    id_nao_existente = uuid.uuid4()

    response = client.get(f'{ROTA}/{id_nao_existente}')

    assert response.status_code == HTTPStatus.NOT_FOUND

    assert response.get_json() == [{'msg': 'Cargo não encontrado.'}]


def test_busca_superiores_oficiais_apenas_cargo_sucesso(
    client: FlaskClient, seed_cargo_oficial_general
):
    response = client.get(f'{ROTA}/{seed_cargo_oficial_general.id}')

    assert response.status_code == HTTPStatus.OK

    assert response.get_json() == {
        'cargo_superior': 'Marechal',
        'fk_cargo_superior_id': str(
            seed_cargo_oficial_general.fk_cargo_superior_id
        ),
        'superiores': [],
    }


def test_busca_superiores_oficiais_sem_cargo_superior(
    client: FlaskClient, seed_cargo_oficial_marechal
):
    response = client.get(f'{ROTA}/{seed_cargo_oficial_marechal.id}')

    assert response.status_code == HTTPStatus.NOT_FOUND

    assert response.get_json() == [{'msg': 'Cargo não possui superior.'}]
