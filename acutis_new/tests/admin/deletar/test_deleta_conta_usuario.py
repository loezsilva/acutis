from http import HTTPStatus

from flask.testing import FlaskClient

from acutis_api.domain.entities.endereco import Endereco
from acutis_api.domain.entities.lead import Lead
from acutis_api.domain.entities.lead_campanha import LeadCampanha
from acutis_api.domain.entities.membro import Membro
from acutis_api.domain.entities.metadado_lead import MetadadoLead
from acutis_api.infrastructure.extensions import database


def test_admin_excluir_conta_usuario_not_found(
    client,
    membro_token,
):
    response = client.delete(
        '/api/admin/membros/excluir-conta/0cee2d74-e7a4-437d-9bf4-2f2daee8b565',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.get_json() == [{'msg': 'Usuário não encontrado.'}]


def test_admin_excluir_conta_usuario(
    client: FlaskClient, membro_token: str, seed_membro_com_todas_relacoes
):
    seed_membro_com_todas_relacoes = seed_membro_com_todas_relacoes()
    lead = seed_membro_com_todas_relacoes['lead']
    membro = seed_membro_com_todas_relacoes['membro']
    endereco = seed_membro_com_todas_relacoes['endereco']
    lead_campanha = seed_membro_com_todas_relacoes['lead_campanha']
    meta_data_lead = seed_membro_com_todas_relacoes['meta_data_lead']

    response = client.delete(
        f'/api/admin/membros/excluir-conta/{lead.id}',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.get_json() == {'msg': 'Conta deletada com sucesso'}

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
