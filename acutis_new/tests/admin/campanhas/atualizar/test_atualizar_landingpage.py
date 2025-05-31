from http import HTTPStatus
from unittest.mock import patch

from flask.testing import FlaskClient

from acutis_api.application.use_cases.campanha.atualizar import (
    AtualizarLandPageCampanhaUseCase,
)
from acutis_api.domain.entities.landing_page import LandingPage
from acutis_api.infrastructure.extensions import database

ROTA = '/api/admin/campanhas/atualizar-landingpage'


def test_atualizar_landingpage_sucesso(
    client: FlaskClient, seed_landingpage_campanha, membro_token
):
    payload = {
        'fk_landingpage_id': (seed_landingpage_campanha.id),
        'conteudo': '<html><body>Conteúdo Atualizado</body></html>',
        'shlink': 'https://novo.link',
        'estrutura_json': """{
            'titulo': 'Título da Página',
            'descricao': 'Descrição da Página',
            'imagem': 'https://example.com/imagem.jpg',
            'cor_fundo': '#FFFFFF',
            'cor_texto': '#000000',
            'cor_botao': '#FF0000',
            'texto_botao': 'Clique Aqui',
            'url_redirecionamento': 'https://example.com/redirecionar',
        }""",
    }

    response = client.put(
        ROTA,
        json=payload,
        headers={
            'Authorization': f'Bearer {membro_token}',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.get_json() == {'msg': 'Landpage atualizada com sucesso.'}
    assert (
        database.session.query(LandingPage)
        .filter(LandingPage.id == seed_landingpage_campanha.id)
        .first()
        .conteudo
    ) == '<html><body>Conteúdo Atualizado</body></html>'


def test_atualizar_landingpage_nao_encontrada(
    client: FlaskClient, membro_token
):
    response = client.put(
        ROTA,
        json={
            'fk_landingpage_id': '6724c907-85cd-46b1-978d-f7279d4c7521',
            'conteudo': '<html><body>Conteúdo Atualizado</body></html>',
            'shlink': 'https://novo.link',
            'estrutura_json': """{
                'titulo': 'Título da Página',
                'descricao': 'Descrição da Página',
                'imagem': 'https://example.com/imagem.jpg',
                'cor_fundo': '#FFFFFF',
                'cor_texto': '#000000',
                'cor_botao': '#FF0000',
                'texto_botao': 'Clique Aqui',
                'url_redirecionamento': 'https://example.com/redirecionar',
            }""",
        },
        headers={
            'Authorization': f'Bearer {membro_token}',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.get_json() == [{'msg': 'Landing page não encontrada'}]


def test_atualizar_landingpage_erro_interno(
    client: FlaskClient, seed_landingpage_campanha, membro_token
):
    with patch.object(
        AtualizarLandPageCampanhaUseCase, 'execute'
    ) as mock_execute:
        mock_execute.side_effect = Exception('Erro interno no servidor')

        response = client.put(
            ROTA,
            json={
                'fk_landingpage_id': seed_landingpage_campanha.id,
                'conteudo': '<html><body>Conteúdo Atualizado</body></html>',
                'shlink': 'https://novo.link',
                'estrutura_json': """{
                'titulo': 'Título da Página',
                'descricao': 'Descrição da Página',
                'imagem': 'https://example.com/imagem.jpg',
                'cor_fundo': '#FFFFFF',
                'cor_texto': '#000000',
                'cor_botao': '#FF0000',
                'texto_botao': 'Clique Aqui',
                'url_redirecionamento': 'https://example.com/redirecionar',
            }""",
            },
            headers={
                'Authorization': f'Bearer {membro_token}',
            },
        )

    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert response.get_json() == [{'msg': 'Erro interno no servidor.'}]
