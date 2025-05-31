from http import HTTPStatus
from unittest.mock import patch

from flask.testing import FlaskClient
from sqlalchemy import select

from acutis_api.application.use_cases.campanha.listar import (
    ListaDeCampanhasUseCase,
)
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


@patch.object(ListaDeCampanhasUseCase, 'execute')
def test_lista_de_campanhas_erro_interno_servidor(
    mock_target, client: FlaskClient, membro_token
):
    mock_target.side_effect = Exception('Erro interno no servidor')

    response = client.get(
        '/api/admin/campanhas/lista-de-campanhas',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert response.json == [{'msg': 'Erro interno no servidor.'}]
