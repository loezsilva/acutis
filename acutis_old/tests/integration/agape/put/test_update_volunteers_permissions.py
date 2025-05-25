from http import HTTPStatus
from flask.testing import FlaskClient
from flask_jwt_extended import create_access_token

from builder import db
from models.menu_sistema import MenuSistema
from models.perfil import Perfil, ProfilesEnum
from models.permissao_menu import PermissaoMenu


def test_update_volunteers_permissions_success(
    test_client: FlaskClient, seed_admin_user_token
):

    perfil = Perfil.query.filter_by(nome=ProfilesEnum.VOLUNTARIO_AGAPE).first()
    permissao_menu: PermissaoMenu = (
        PermissaoMenu.query.join(
            Perfil, PermissaoMenu.fk_perfil_id == Perfil.id
        )
        .join(MenuSistema, PermissaoMenu.fk_menu_id == MenuSistema.id)
        .filter(
            Perfil.id == perfil.id,
            MenuSistema.slug == "familia_agape",
        )
        .first()
    )
    permissao_anterior_acessar = permissao_menu.acessar
    permissao_anterior_criar = permissao_menu.criar
    permissao_anterior_editar = permissao_menu.editar

    response = test_client.put(
        "/agape/atualizar-permissoes-voluntarios",
        headers=seed_admin_user_token,
    )

    assert response.status_code == HTTPStatus.NO_CONTENT
    db.session.refresh(permissao_menu)

    assert permissao_menu.acessar != permissao_anterior_acessar
    assert permissao_menu.criar != permissao_anterior_criar
    assert permissao_menu.editar != permissao_anterior_editar


def test_update_volunteers_permissions_error_forbidden(
    test_client: FlaskClient, seed_user_with_dependencies
):
    user, _, _, _ = seed_user_with_dependencies
    token = create_access_token(identity=user.id)

    response = test_client.put(
        "/agape/atualizar-permissoes-voluntarios",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json == {
        "error": "Você não tem permissão para realizar esta ação."
    }
