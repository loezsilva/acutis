from http import HTTPStatus
from flask.testing import FlaskClient

from models.schemas.agape.get.get_agape_member import GetAgapeMemberResponse


def test_get_agape_member_success(
    test_client: FlaskClient, seed_admin_user_token, seed_agape_member
):
    membro = seed_agape_member
    expected = GetAgapeMemberResponse(
        id=membro.id,
        cpf=membro.cpf,
        data_nascimento=membro.data_nascimento.strftime("%Y-%m-%d"),
        email=membro.email,
        escolaridade=membro.escolaridade,
        funcao_familiar=membro.funcao_familiar,
        nome=membro.nome,
        ocupacao=membro.ocupacao,
        renda=membro.renda,
        responsavel=membro.responsavel,
        telefone=membro.telefone,
    )

    response = test_client.get(
        f"/agape/buscar-membro/{membro.id}", headers=seed_admin_user_token
    )

    assert response.status_code == HTTPStatus.OK


def test_get_agape_member_error_member_not_found(
    test_client: FlaskClient, seed_admin_user_token
):
    response = test_client.get(
        "/agape/buscar-membro/9999", headers=seed_admin_user_token
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json == {"error": "Membro não encontrado."}
