from time import sleep
from flask.testing import FlaskClient
from builder import db
from models.leads_sorteados import LeadsSorteados

from utils.functions import get_current_time


def test_confirm_selected_lead_register_winner_success(
    test_client: FlaskClient, seed_actions_and_leads, seed_admin_user_token
):
    action, _ = seed_actions_and_leads

    payload = {
        "acao_id": action.id,
        "nome": "Novo Lead Sorteado",
        "email": "novolead@headers.com.br",
    }

    response = test_client.post(
        "/administradores/confirmar-lead-sorteado",
        json=payload,
        content_type="application/json",
        headers=seed_admin_user_token,
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["msg"] == "O sorteio foi registrado com sucesso!"

    lead = (
        db.session.query(LeadsSorteados)
        .filter_by(email="novolead@headers.com.br")
        .first()
    )
    assert lead is not None
    assert lead.nome == "Novo Lead Sorteado"
    assert lead.sorteador == 1
    assert lead.acao_sorteada == action.id
    assert lead.data_sorteio.date() == get_current_time().date()

    db.session.refresh(action)
    assert action.sorteio == True

    db.session.delete(lead)
    db.session.commit()


def test_confirm_selected_lead_override_winner_success(
    test_client: FlaskClient, seed_actions_and_leads, seed_admin_user_token
):
    action, lead = seed_actions_and_leads

    payload = {
        "acao_id": action.id,
        "lead_sorteado_id": lead.id,
        "nome": "Lead Atualizado",
        "email": "atualizado@headers.com.br",
    }

    query_params = {"sobrepor_sorteio": True}

    sleep(1)

    response = test_client.post(
        f"/administradores/confirmar-lead-sorteado?sobrepor_sorteio={query_params['sobrepor_sorteio']}",
        json=payload,
        content_type="application/json",
        headers=seed_admin_user_token,
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["msg"] == "O sorteio foi registrado com sucesso!"

    db.session.refresh(lead)
    assert lead.nome == "Lead Atualizado"
    assert lead.email == "atualizado@headers.com.br"
    assert lead.sorteador == 1
    assert lead.data_sorteio.date() == get_current_time().date()

    db.session.refresh(action)
    assert action.sorteio == True
