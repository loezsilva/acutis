from http import HTTPStatus
from unittest.mock import patch

from flask.testing import FlaskClient

from acutis_api.application.use_cases.campanha.registrar import (
    SalvarLandPageCampanhaUseCase,
)
from acutis_api.domain.entities.landing_page import LandingPage
from acutis_api.infrastructure.extensions import database

ROTA = '/api/admin/campanhas/registrar-landingpage'


def test_registrar_landingpage(
    client: FlaskClient, seed_campanha_cadastro_sem_landingpage, membro_token
):
    response = client.post(
        ROTA,
        json={
            'nome_campanha': seed_campanha_cadastro_sem_landingpage.nome,
            'conteudo': '<html><body>Teste</body></html>',
            'shlink': None,
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

    assert response.status_code == HTTPStatus.CREATED
    assert response.get_json() == {'msg': 'Landpage salva com sucesso.'}

    verificar_landing_page = database.session.query(LandingPage).filter(
        LandingPage.fk_campanha_id == seed_campanha_cadastro_sem_landingpage.id
    )

    assert verificar_landing_page is not None


def test_registrar_landingpage_conflict(
    client: FlaskClient, seed_campanha_cadastro, membro_token
):
    response = client.post(
        ROTA,
        json={
            'nome_campanha': seed_campanha_cadastro.nome,
            'conteudo': '<html><body>Teste</body></html>',
            'shlink': None,
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

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.get_json() == [
        {'msg': 'Essa campanha já possui uma landing page'}
    ]


def test_registrar_landingpage_campanha_not_found(
    client: FlaskClient, membro_token
):
    response = client.post(
        ROTA,
        json={
            'nome_campanha': 'Campanha Inexistente',
            'conteudo': '<html><body>Teste</body></html>',
            'shlink': None,
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
    assert response.get_json() == [{'msg': 'Campanha não encontrada'}]


@patch.object(SalvarLandPageCampanhaUseCase, 'execute')
def test_confirmar_exclusao_conta_erro_interno_servidor(
    mock_target, client: FlaskClient, membro_token
):
    mock_target.side_effect = Exception('Erro interno no servidor')

    response = client.post(
        ROTA,
        json={
            'nome_campanha': 'Campanha Inexistente',
            'conteudo': '<html><body>Teste</body></html>',
            'shlink': None,
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
    assert response.json == [{'msg': 'Erro interno no servidor.'}]
