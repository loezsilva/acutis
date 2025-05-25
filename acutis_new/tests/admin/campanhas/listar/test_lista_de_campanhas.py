from http import HTTPStatus

from flask.testing import FlaskClient
from sqlalchemy import select

from acutis_api.domain.entities.campanha import Campanha
from acutis_api.infrastructure.extensions import database


def test_list_de_campanhas(
    client: FlaskClient,
    seed_campanha_cadastro,
    seed_campanha_doacao,
    membro_token,
):
    campanhas = database.session.scalars(
        select(Campanha).order_by(Campanha.nome)
    ).all()

    response = client.get(
        '/api/admin/campanhas/lista-de-campanhas',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK

    assert response.get_json() == [
        {
            'id': str(campanha.id),
            'nome_campanha': campanha.nome,
        }
        for campanha in campanhas
    ]
