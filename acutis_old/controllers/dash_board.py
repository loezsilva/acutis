from flask import jsonify, Blueprint
from exceptions.errors_handler import errors_handler
from handlers.dashboard_users.amount_value_donation import AmountValueDonations
from handlers.dashboard_users.cadastros_do_dia_por_hora import (
    UsersPerHourDaily,
)
from handlers.dashboard_users.card_media_cadastros_mensal import (
    CadastrosMediaMensal,
)
from handlers.dashboard_users.card_media_diaria import MediaCadastrosDiarios
from handlers.dashboard_users.card_uses_actual_month import UsersActualMonth
from handlers.dashboard_users.progress_months import UserProgressByMonth
from handlers.dashboard_users.user_by_months import UsersByMonths
from handlers.dashboard_users.users_actives import UserActives
from handlers.dashboard_users.users_by_age import UserByAge
from handlers.dashboard_users.users_by_region import UsersAndCampaignsByRegion
from handlers.dashboard_users.users_by_state import UsersByState
from handlers.dashboard_users.users_per_campaigns import UsersPerCampaigns
from handlers.dashboard_users.users_per_hours import UsersByHours
from handlers.dashboard_users.users_per_weekday import UsersByWeekday
from models import (
    Usuario,
)
from builder import db, api
from flask_jwt_extended import jwt_required
from utils.verify_permission import permission_required
from spectree import Response
from utils.response import DefaultErrorResponseSchema, response_handler
from models.usuario import (
    DashBoardCountUsers,
    DashBoardActiveUsers,
    DashBoardProgressByDayOfWeek,
    DashBoardProgressByHours,
    DashBoardUsersByCampaign,
    DashBoardAmountDonations,
    DashBoardUsersByAge,
    CadastrosPorMesSchema,
    DashBordProgressUsersByMonth,
    DashBoardUsersByState,
    ResponseSchemaCadasMensal,
    ResponseSchemaCadasDiario,
)

dash_board = Blueprint(
    "dash_board", __name__, url_prefix="/admin/dash-board/users"
)


@dash_board.get("/count-users")
@api.validate(
    resp=Response(
        HTTP_200=DashBoardCountUsers,
        HTTP_403=DefaultErrorResponseSchema,
        HTTP_404=DefaultErrorResponseSchema,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["DashBoard"],
)
@jwt_required()
@permission_required("dash_board_users", "acessar")
def count_users():
    """
    Retorna a quantidade de usuário cadastrados no sistema.
    """
    try:
        count_users = (
            db.session.query(Usuario)
            .filter(Usuario.deleted_at == None)
            .count()
        )
        response = {"count_users": count_users}

        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@dash_board.get("/active-users")
@api.validate(
    resp=Response(
        HTTP_200=DashBoardActiveUsers,
        HTTP_403=DefaultErrorResponseSchema,
        HTTP_404=DefaultErrorResponseSchema,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["DashBoard"],
)
@jwt_required()
@permission_required("dash_board_users", "acessar")
def users_actives():
    """
    Retorna análise de usuarios ativos e inativos
    """
    try:
        get_users_actives = UserActives(db)
        response = response_handler(get_users_actives.execute())
        return response
    except Exception as e:
        response_error = errors_handler(e)
        return response_error


@dash_board.get("/users-by-month")
@api.validate(
    resp=Response(
        HTTP_200=CadastrosPorMesSchema,
        HTTP_403=DefaultErrorResponseSchema,
        HTTP_404=DefaultErrorResponseSchema,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["DashBoard"],
)
@jwt_required()
@permission_required("dash_board_users", "acessar")
def users_by_month():
    """
    Retorna a quantidade de cadastros por mês dos últimos 12 meses.
    """
    try:
        users_by_months = UsersByMonths(db)
        response = response_handler(users_by_months.execute())
        return response
    except Exception as e:
        response_error = errors_handler(e)
        return response_error


@dash_board.get("/progress-count-users")
@api.validate(
    resp=Response(
        HTTP_200=DashBordProgressUsersByMonth,
        HTTP_403=DefaultErrorResponseSchema,
        HTTP_404=DefaultErrorResponseSchema,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["DashBoard"],
)
@jwt_required()
@permission_required("dash_board_users", "acessar")
def progress_count_users():
    """
    Retorna o progresso do número de usuários cadastrados a cada mês.
    """
    try:
        progress_by_months = UserProgressByMonth(db)
        response = response_handler(progress_by_months.execute())
        return response
    except Exception as e:
        response_error = errors_handler(e)
        return response_error


@dash_board.get("/users-by-weekday")
@api.validate(
    resp=Response(
        HTTP_200=DashBoardProgressByDayOfWeek,
        HTTP_403=DefaultErrorResponseSchema,
        HTTP_404=DefaultErrorResponseSchema,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["DashBoard"],
)
@jwt_required()
@permission_required("dash_board_users", "acessar")
def users_by_weekday():
    """
    Retorna quantidade de usuários cadastrados por dia da semana
    """
    try:
        per_weekday = UsersByWeekday(db)
        response = response_handler(per_weekday.execute())
        return response
    except Exception as e:
        response_error = errors_handler(e)
        return response_error


@dash_board.get("/users-by-hours")
@api.validate(
    resp=Response(
        HTTP_200=DashBoardProgressByHours,
        HTTP_403=DefaultErrorResponseSchema,
        HTTP_404=DefaultErrorResponseSchema,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["DashBoard"],
)
@jwt_required()
@permission_required("dash_board_users", "acessar")
def users_by_hours():
    """
    Retornar análise de cadastros de usuários por hora.
    """
    try:
        get_by_hours = UsersByHours(db)
        response = response_handler(get_by_hours.execute())
        return response

    except Exception as e:
        response_error = errors_handler(e)
        return response_error


@dash_board.get("/users-by-state")
@api.validate(
    resp=Response(
        HTTP_200=DashBoardUsersByState,
        HTTP_403=DefaultErrorResponseSchema,
        HTTP_404=DefaultErrorResponseSchema,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["DashBoard"],
)
@jwt_required()
@permission_required("dash_board_users", "acessar")
def user_by_state():
    """Retorna a quantidade de usuários por estado"""
    try:
        get_by_state = UsersByState(db)
        response = response_handler(get_by_state.execute())
        return response
    except Exception as err:
        response_error = errors_handler(err)
        response = response_error


@dash_board.get("/users-by-region")
@api.validate(
    resp=Response(
        HTTP_200=None,
        HTTP_403=DefaultErrorResponseSchema,
        HTTP_404=DefaultErrorResponseSchema,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["DashBoard"],
)
@jwt_required()
@permission_required("dash_board_users", "acessar")
def users_and_campaigns_by_region():
    """
    Retorna análise de usuários e campanhas por região com paginação manual aplicada à lista de campanhas mais populares.
    """
    try:
        get_by_region = UsersAndCampaignsByRegion(db)
        return response_handler(get_by_region.execute())
    except Exception as err:
        response_error = errors_handler(err)
        return response_error


@dash_board.get("/users-per-campaign")
@api.validate(
    resp=Response(
        HTTP_200=DashBoardUsersByCampaign,
        HTTP_403=DefaultErrorResponseSchema,
        HTTP_404=DefaultErrorResponseSchema,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["DashBoard"],
)
@jwt_required()
@permission_required("dash_board_users", "acessar")
def user_per_campaign():
    """
    Retorna a quantidade de cadastros por campanha
    """
    try:
        per_campaigns = UsersPerCampaigns(db)
        response = response_handler(per_campaigns.execute())
        return response
    except Exception as err:
        response_error = errors_handler(err)
        return response_error


@dash_board.get("/amount_value_donation")
@api.validate(
    resp=Response(
        HTTP_200=DashBoardAmountDonations,
        HTTP_403=DefaultErrorResponseSchema,
        HTTP_404=DefaultErrorResponseSchema,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["DashBoard"],
)
@jwt_required()
@permission_required("dash_board_donations", "acessar")
def amount_value_donations():
    """
    Retorna valor total de doações atual.
    """
    try:
        get_total = AmountValueDonations(db)
        response = response_handler(get_total.execute())
        return response
    except Exception as er:
        response_error = errors_handler(er)
        return response_error


@dash_board.get("/users-by-age")
@api.validate(
    resp=Response(
        HTTP_200=DashBoardUsersByAge,
        HTTP_403=DefaultErrorResponseSchema,
        HTTP_404=DefaultErrorResponseSchema,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["DashBoard"],
)
@jwt_required()
@permission_required("dash_board_users", "acessar")
def user_by_age():
    try:
        by_age = UserByAge(db)
        response = response_handler(by_age.execute())
        return response
    except Exception as er:
        response_error = errors_handler(e)
        return response_error


@dash_board.get("/actual-month")
@jwt_required()
@permission_required("dash_board_users", "acessar")
def users_actual_month():
    """Retorna a quantidade de cadastros por dia no mês atual"""
    try:
        actual_month = UsersActualMonth(db)
        response = response_handler(actual_month.execute())
        return response
    except Exception as err:
        response_error = errors_handler(err)
        return response_error


@dash_board.get("/quantidade-cadastros-diario")
@api.validate(
    resp=Response(
        HTTP_200=ResponseSchemaCadasDiario,
        HTTP_403=DefaultErrorResponseSchema,
        HTTP_404=DefaultErrorResponseSchema,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["DashBoard"],
)
@jwt_required()
@permission_required("dash_board_users", "acessar")
def media_cadastros_diario():
    """Retorna a media de cadastros diário"""
    try:
        get_media = MediaCadastrosDiarios(db)
        response = response_handler(get_media.execute())
        return response
    except Exception as err:
        response_error = errors_handler(err)
        return response_error


@dash_board.get("/quantidade-cadastros-mensal")
@api.validate(
    resp=Response(
        HTTP_200=ResponseSchemaCadasMensal,
        HTTP_403=DefaultErrorResponseSchema,
        HTTP_404=DefaultErrorResponseSchema,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["DashBoard"],
)
@jwt_required()
@permission_required("dash_board_users", "acessar")
def cadastros_media_mensal():
    """Retorna a média de cadastros mensal"""
    try:
        media_mensal = CadastrosMediaMensal(db)
        response = response_handler(media_mensal.execute())
        return response
    except Exception as e:
        response_error = errors_handler(e)
        return response_error


@dash_board.get("/cadastros-diario-per-hour")
@api.validate(
    query=None,
    resp=Response(
        HTTP_200=None,
        HTTP_403=DefaultErrorResponseSchema,
        HTTP_404=DefaultErrorResponseSchema,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["DashBoard"],
)
@jwt_required()
@permission_required("dash_board_users", "acessar")
def users_per_hour_daily():
    """Retorna o número de cadastros diários por hora!"""
    try:
        daily = UsersPerHourDaily(db)
        return response_handler(daily.execute())
    except Exception as e:
        response_error = errors_handler(e)
        return response_error
