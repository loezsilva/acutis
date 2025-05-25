from http import HTTPStatus
from flask.testing import FlaskClient
from flask_jwt_extended import create_access_token

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
    status = all(
        [permissao_menu.acessar, permissao_menu.criar, permissao_menu.editar]
    )

    response = test_client.get(
        "/agape/status-permissao-voluntarios",
        headers=seed_admin_user_token,
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json == {"status": status}


def test_get_volunteers_permissions_status_error_forbidden(
    test_client: FlaskClient, seed_user_with_dependencies
):
    user, _, _, _ = seed_user_with_dependencies
    token = create_access_token(identity=user.id)

    response = test_client.get(
        "/agape/status-permissao-voluntarios",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json == {
        "error": "Você não tem permissão para realizar esta ação."
    }
