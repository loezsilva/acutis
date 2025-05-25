import uuid
from http import HTTPStatus

import pytest
from flask.testing import FlaskClient

from acutis_api.domain.entities.campanha import Campanha
from acutis_api.infrastructure.extensions import database
from tests.factories import (
    BenfeitorFactory,
    DoacaoFactory,
    PagamentoDoacaoFactory,
    ProcessamentoDoacaoFactory,
)


@pytest.fixture
def seed_benfeitor_doacao():
    def _benfeitor_doacao(*, campanha: Campanha, nome: str):
        benfeitor1 = BenfeitorFactory(numero_documento=65086880068, nome=nome)
        database.session.add(benfeitor1)

        doacao1 = DoacaoFactory(
            fk_benfeitor_id=benfeitor1.id,
            fk_campanha_doacao_id=campanha.campanha_doacao.id,
        )
        database.session.add(doacao1)

        pagamento_doacao = PagamentoDoacaoFactory(
            fk_doacao_id=doacao1.id,
            codigo_ordem_pagamento=str(uuid.uuid4()),
            recorrente=False,
        )
        database.session.add(pagamento_doacao)

        processamento_doacao = ProcessamentoDoacaoFactory(
            fk_pagamento_doacao_id=pagamento_doacao.id,
            codigo_referencia=str(uuid.uuid4()),
        )
        database.session.add(processamento_doacao)
        database.session.commit()

    return _benfeitor_doacao


def test_listar_doacoes_sucesso(
    client: FlaskClient,
    membro_token,
    seed_campanha_doacao,
    seed_dados_doacao,
    seed_benfeitor_doacao,
):
    total_registros = 2

    campanha = seed_campanha_doacao
    seed_dados_doacao(campanha=campanha, doacao_ativa=True)
    seed_benfeitor_doacao(campanha=campanha, nome='Yanzin Cortador de Cebolas')

    response = client.get(
        '/api/admin/doacoes/listar-doacoes',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json['total'] == total_registros


def test_listar_doacoes_filtro_ordenar_ascendente(
    client: FlaskClient,
    membro_token,
    seed_campanha_doacao,
    seed_dados_doacao,
    seed_benfeitor_doacao,
):
    total_registros = 2

    campanha = seed_campanha_doacao
    seed_dados_doacao(campanha=campanha, doacao_ativa=True)
    seed_benfeitor_doacao(campanha=campanha, nome='aaaaaa')

    response = client.get(
        '/api/admin/doacoes/listar-doacoes?ordenar_por=benfeitor_nome&tipo_ordenacao=asc',  # noqa
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json['total'] == total_registros
    assert response.json['doacoes'][0]['benfeitor']['nome'] == 'aaaaaa'


def test_listar_doacoes_filtro_nome(
    client: FlaskClient,
    membro_token,
    seed_campanha_doacao,
    seed_dados_doacao,
    seed_benfeitor_doacao,
):
    total_registros = 1

    campanha = seed_campanha_doacao
    seed_dados_doacao(campanha=campanha, doacao_ativa=True)
    seed_benfeitor_doacao(
        campanha=campanha,
        nome='Neville Guimarães',  # NOSONAR
    )
    response = client.get(
        '/api/admin/doacoes/listar-doacoes?nome_email_documento=nevi',  # noqa
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json['total'] == total_registros
    assert response.json['doacoes'][0]['benfeitor']['nome'] == (
        'Neville Guimarães'
    )


def test_listar_doacoes_filtro_campanha_id(
    client: FlaskClient,
    membro_token,
    seed_campanha_doacao,
    seed_dados_doacao,
    seed_benfeitor_doacao,
):
    total_registros = 2

    campanha = seed_campanha_doacao
    seed_dados_doacao(campanha=campanha, doacao_ativa=True)
    seed_benfeitor_doacao(campanha=campanha, nome='Neville Guimarães')

    response = client.get(
        f'/api/admin/doacoes/listar-doacoes?campanha_id={campanha.id}',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json['total'] == total_registros


def test_listar_doacoes_filtro_campanha_nome(
    client: FlaskClient,
    membro_token,
    seed_campanha_doacao,
    seed_dados_doacao,
    seed_benfeitor_doacao,
):
    total_registros = 2

    campanha = seed_campanha_doacao
    seed_dados_doacao(campanha=campanha, doacao_ativa=True)
    seed_benfeitor_doacao(campanha=campanha, nome='Neville Guimarães')

    response = client.get(
        f'/api/admin/doacoes/listar-doacoes?campanha_nome={campanha.nome}',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json['total'] == total_registros


def test_listar_doacoes_filtro_recorrente(
    client: FlaskClient,
    membro_token,
    seed_campanha_doacao,
    seed_dados_doacao,
    seed_benfeitor_doacao,
):
    total_registros = 1

    campanha = seed_campanha_doacao
    seed_dados_doacao(campanha=campanha, doacao_ativa=True)
    seed_benfeitor_doacao(campanha=campanha, nome='Neville Guimarães')

    response = client.get(
        '/api/admin/doacoes/listar-doacoes?recorrente=true',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json['total'] == total_registros


def test_listar_doacoes_filtro_forma_pagamento(
    client: FlaskClient,
    membro_token,
    seed_campanha_doacao,
    seed_dados_doacao,
    seed_benfeitor_doacao,
):
    total_registros = 2

    campanha = seed_campanha_doacao
    seed_dados_doacao(campanha=campanha, doacao_ativa=True)
    seed_benfeitor_doacao(campanha=campanha, nome='Neville Guimarães')

    response = client.get(
        '/api/admin/doacoes/listar-doacoes?forma_pagamento=credito',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json['total'] == total_registros


def test_listar_doacoes_filtro_anonimo(
    client: FlaskClient,
    membro_token,
    seed_campanha_doacao,
    seed_dados_doacao,
    seed_benfeitor_doacao,
):
    total_registros = 0

    campanha = seed_campanha_doacao
    seed_dados_doacao(campanha=campanha, doacao_ativa=True)
    seed_benfeitor_doacao(campanha=campanha, nome='Neville Guimarães')

    response = client.get(
        '/api/admin/doacoes/listar-doacoes?anonimo=true',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json['total'] == total_registros


def test_listar_doacoes_filtro_gateway(
    client: FlaskClient,
    membro_token,
    seed_campanha_doacao,
    seed_dados_doacao,
    seed_benfeitor_doacao,
):
    total_registros = 2

    campanha = seed_campanha_doacao
    seed_dados_doacao(campanha=campanha, doacao_ativa=True)
    seed_benfeitor_doacao(campanha=campanha, nome='Neville Guimarães')

    response = client.get(
        '/api/admin/doacoes/listar-doacoes?gateway=maxipago',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json['total'] == total_registros


def test_listar_doacoes_filtro_ativo(
    client: FlaskClient,
    membro_token,
    seed_campanha_doacao,
    seed_dados_doacao,
    seed_benfeitor_doacao,
):
    total_registros = 1

    campanha = seed_campanha_doacao
    seed_dados_doacao(campanha=campanha, doacao_ativa=False)
    seed_benfeitor_doacao(campanha=campanha, nome='Neville Guimarães')

    response = client.get(
        '/api/admin/doacoes/listar-doacoes?ativo=true',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json['total'] == total_registros


def test_listar_doacoes_filtro_status(
    client: FlaskClient,
    membro_token,
    seed_campanha_doacao,
    seed_dados_doacao,
    seed_benfeitor_doacao,
):
    total_registros = 2

    campanha = seed_campanha_doacao
    seed_dados_doacao(campanha=campanha, doacao_ativa=False)
    seed_benfeitor_doacao(campanha=campanha, nome='Neville Guimarães')

    response = client.get(
        '/api/admin/doacoes/listar-doacoes?status=pago',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json['total'] == total_registros
