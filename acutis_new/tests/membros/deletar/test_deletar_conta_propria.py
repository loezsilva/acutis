import json
from http import HTTPStatus
from unittest.mock import patch

from flask.testing import FlaskClient

from acutis_api.application.use_cases.membros.deletar import (
    ConfirmaExclusaoContaUseCase,
)
from acutis_api.application.use_cases.membros.deletar.excluir_conta import (
    ExcluirContaUseCase,
)
from acutis_api.application.utils.funcoes_auxiliares import (
    TokenSaltEnum,
    gerar_token,
)
from acutis_api.domain.entities.endereco import Endereco
from acutis_api.domain.entities.lead import Lead
from acutis_api.domain.entities.lead_campanha import LeadCampanha
from acutis_api.domain.entities.membro import Membro
from acutis_api.domain.entities.metadado_lead import MetadadoLead
from acutis_api.infrastructure.extensions import database


def test_usuario_solicita_exclusao_de_conta(
    client: FlaskClient,
    membro_token,
):
    response = client.get(
        '/api/membros/excluir-conta',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK

    assert response.get_json() == {
        'msg': 'Verifique sua solicitação de exclusão em seu e-mail.',
    }


def test_usuario_confirma_exclusao_de_conta(
    client: FlaskClient,
    seed_membro_com_todas_relacoes,
):
    seed_membro_com_todas_relacoes = seed_membro_com_todas_relacoes()
    lead = seed_membro_com_todas_relacoes['lead']
    membro = seed_membro_com_todas_relacoes['membro']
    endereco = seed_membro_com_todas_relacoes['endereco']
    lead_campanha = seed_membro_com_todas_relacoes['lead_campanha']
    meta_data_lead = seed_membro_com_todas_relacoes['meta_data_lead']

    payload = {'email': lead.email, 'fk_lead_id': str(lead.id)}

    token = gerar_token(payload, TokenSaltEnum.excluir_conta)

    response = client.delete(
        '/api/membros/confirma-exclusao-de-conta',
        data=json.dumps({'token': token}),
        content_type='application/json',
    )

    assert response.status_code == HTTPStatus.OK

    verify_lead = (
        database.session.query(Lead).filter(Lead.id == lead.id).first()
    )

    assert verify_lead is None

    verify_membro = (
        database.session.query(Membro).filter(Membro.id == membro.id).first()
    )

    assert verify_membro is None

    verify_endereco = (
        database.session.query(Endereco)
        .filter(Endereco.id == endereco.id)
        .first()
    )

    assert verify_endereco is None

    verify_lead_campanha = (
        database.session.query(LeadCampanha)
        .filter(LeadCampanha.id == lead_campanha.id)
        .first()
    )

    assert verify_lead_campanha is None

    verify_meta_data_lead = (
        database.session.query(MetadadoLead)
        .filter(MetadadoLead.id == meta_data_lead.id)
        .first()
    )

    assert verify_meta_data_lead is None


@patch.object(ExcluirContaUseCase, 'execute')
def test_deletar_conta_erro_interno_servidor(
    mock_target, client: FlaskClient, membro_token
):
    mock_target.side_effect = Exception('Erro interno no servidor')

    response = client.get(
        '/api/membros/excluir-conta',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert response.json == [{'msg': 'Erro interno no servidor.'}]


@patch.object(ConfirmaExclusaoContaUseCase, 'execute')
def test_confirmar_exclusao_conta_erro_interno_servidor(
    mock_target, client: FlaskClient, membro_token
):
    mock_target.side_effect = Exception('Erro interno no servidor')

    response = client.delete(
        '/api/membros/confirma-exclusao-de-conta',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert response.json == [{'msg': 'Erro interno no servidor.'}]
