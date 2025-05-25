from typing import Optional
from flask import Blueprint
from exceptions.errors_handler import errors_handler
from handlers.dashboard_donations.campaigns_donations import DonationsCampaign
from handlers.dashboard_donations.card_media_mensal import MediaMensalDonations
from handlers.dashboard_donations.card_media_weekday import (
    MediaDiariaDonations,
)
from handlers.dashboard_donations.card_total_dia_atual import (
    TotalDonationsActualDay,
)
from handlers.dashboard_donations.card_total_do_mes import (
    TotalDonationsActualMonth,
)
from handlers.dashboard_donations.card_total_value import CardTotalValue
from handlers.dashboard_donations.card_user_donations_total import (
    UserTotalDonation,
)
from handlers.dashboard_donations.card_valor_total_do_dia import (
    TotalDailyDonations,
)
from handlers.dashboard_donations.doacoces_por_horas_do_dia_atual import (
    DonationsPerHoursNow,
)
from handlers.dashboard_donations.donantions_per_weekday import (
    DonationsPerWeekDay,
)
from handlers.dashboard_donations.donations_actual_month import (
    DonationsActualMonth,
)
from handlers.dashboard_donations.donations_anonimous import DonationsAnonimous
from handlers.dashboard_donations.donations_by_months import DonationsByMonth
from handlers.dashboard_donations.donations_per_type import DonatinonsPerType
from handlers.dashboard_donations.donations_recorrentes_actual_month import (
    DonationsMesAtualApuradas,
)
from handlers.dashboard_donations.donatons_per_hours import DonationsPerHours
from handlers.dashboard_donations.per_method_payment import PerMethodPayment
from handlers.dashboard_donations.progress_by_months import ProgressByMonths
from handlers.dashboard_donations.card_user_donations_actual_month import (
    DonationsUserActualMonth,
)
from handlers.dashboard_donations.total_recorentes_mes_atual import (
    DonationsMesRecorrente,
)
from pydantic import BaseModel
from builder import db, api
from utils.response import DefaultErrorResponseSchema, response_handler
from spectree import Response
from flask_jwt_extended import jwt_required
from utils.verify_permission import permission_required
from models.pedido import (
    DonationItem,
    DonationProgressResponse,
    DonationStatsResponse,
    TotalDonations,
    TotalDonationsDaily,
    MediaMensal,
    UserTotalDonations,
)

dash_board_donations = Blueprint(
    "dash_board_donations", __name__, url_prefix="/admin/dash-board/donations"
)


class DashboardFilterQuery(BaseModel):
    fk_campanha_id: Optional[int | str]
    forma_pagamento: Optional[int]
    data_inicio: Optional[str]
    data_fim: Optional[str]


@dash_board_donations.get("/progress-amount-donations")
@api.validate(
    query=DashboardFilterQuery,
    resp=Response(
        HTTP_200=DonationProgressResponse,
        HTTP_403=DefaultErrorResponseSchema,
        HTTP_404=DefaultErrorResponseSchema,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["DashBoard"],
)
@jwt_required()
@permission_required("dash_board_donations", "acessar")
def progress_amount_donations():
    """
    Retorna o progresso do valor total de doações dos últimos 12 meses.
    """
    try:

        progress = ProgressByMonths(db)
        response = response_handler(progress.execute(), save_logs=False)

        return response

    except Exception as e:
        response_error = errors_handler(e, save_logs=False)
        return response_error


@dash_board_donations.get("/donations-values-by-method-payment")
@api.validate(
    query=DashboardFilterQuery,
    resp=Response(
        HTTP_200=DonationStatsResponse,
        HTTP_403=DefaultErrorResponseSchema,
        HTTP_404=DefaultErrorResponseSchema,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["DashBoard"],
)
@jwt_required()
@permission_required("dash_board_donations", "acessar")
def donations_per_month_and_method():
    """
    Retorna os valores arrecadados por método de pagamento e suas porcentagens, usando uma única consulta.
    """
    try:
        get_methods_payment = PerMethodPayment(db)
        response = response_handler(
            get_methods_payment.execute(), save_logs=True
        )
        return response
    except Exception as e:
        response_error = errors_handler(e, save_logs=True)
        return response_error


@dash_board_donations.get("/donations-per-hours")
@api.validate(
    query=DashboardFilterQuery,
    resp=Response(
        HTTP_200=None,
        HTTP_403=DefaultErrorResponseSchema,
        HTTP_404=DefaultErrorResponseSchema,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["DashBoard"],
)
@jwt_required()
@permission_required("dash_board_donations", "acessar")
def donations_per_hours():
    """
    Retorna a análise da quantidade de doações por horas.
    """

    try:
        get_by_hours = DonationsPerHours(db)
        response = response_handler(get_by_hours.execute(), save_logs=False)
        return response
    except Exception as e:
        response_error = errors_handler(e, save_logs=False)
        return response_error


@dash_board_donations.get("/donations-per-weekday")
@api.validate(
    query=DashboardFilterQuery,
    resp=Response(HTTP_200=None, HTTP_403=None, HTTP_404=None, HTTP_500=None),
    tags=["DashBoard"],
)
@jwt_required()
@permission_required("dash_board_donations", "acessar")
def donation_per_weekday():
    """
    Detalhes de doações por dia da semana e métodos de pagamentos.
    """
    try:
        get_weekdays = DonationsPerWeekDay(db)
        response = response_handler(get_weekdays.execute(), save_logs=False)
        return response

    except Exception as e:
        response_error = errors_handler(e, save_logs=False)
        return response_error


@dash_board_donations.get("/donations-by-months")
@api.validate(
    query=DashboardFilterQuery,
    resp=Response(
        HTTP_200=None,
        HTTP_403=DefaultErrorResponseSchema,
        HTTP_404=DefaultErrorResponseSchema,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["DashBoard"],
)
@jwt_required()
@permission_required("dash_board_donations", "acessar")
def donations_by_month():
    """Retorna valores de doações por meses e métodos de doação."""
    try:
        by_months = DonationsByMonth(db)
        response = response_handler(by_months.execute())
        return response
    except Exception as e:
        response_error = errors_handler(e)
        return response_error


@dash_board_donations.get("/values-donations-anonimous")
@api.validate(
    query=DashboardFilterQuery,
    resp=Response(
        HTTP_200=None,
        HTTP_403=DefaultErrorResponseSchema,
        HTTP_404=DefaultErrorResponseSchema,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["DashBoard"],
)
@jwt_required()
@permission_required("dash_board_donations", "acessar")
def value_donations_anonimous():
    """Retorna quantidade de valores arrecadados de forma anônima e não anônima;"""
    try:
        get_anonimous = DonationsAnonimous(db)
        response = response_handler(get_anonimous.execute(), save_logs=False)
        return response
    except Exception as e:
        response_error = errors_handler(e, save_logs=False)
        return response_error


@dash_board_donations.get("/campaigns-donations")
@api.validate(
    query=DashboardFilterQuery,
    resp=Response(HTTP_200=None, HTTP_500=None),
    tags=["DashBoard"],
)
@jwt_required()
@permission_required("dash_board_donations", "acessar")
def donations_campaign():
    """Retornar arrecadações por campanha"""
    try:
        get_by_campaings = DonationsCampaign(db)
        response = response_handler(get_by_campaings.execute(), save_logs=True)
        return response
    except Exception as e:
        response_error = errors_handler(e, save_logs=True)
        return response_error


@dash_board_donations.get("/donations-actual-month")
@api.validate(
    query=DashboardFilterQuery,
    resp=Response(
        HTTP_200=None,
        HTTP_403=DefaultErrorResponseSchema,
        HTTP_404=DefaultErrorResponseSchema,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["DashBoard"],
)
@jwt_required()
@permission_required("dash_board_donations", "acessar")
def daily_donations():
    """Retorna os valores totais das doações diárias considerando o mês atual."""
    try:
        donations_actual_month = DonationsActualMonth(db)
        response = response_handler(
            donations_actual_month.execute(), save_logs=False
        )
        return response
    except Exception as e:
        response_error = errors_handler(e, save_logs=False)
        return response_error


@dash_board_donations.get("/donations-per-type")
@api.validate(
    query=DashboardFilterQuery,
    resp=Response(
        HTTP_200=None,
        HTTP_403=DefaultErrorResponseSchema,
        HTTP_404=DefaultErrorResponseSchema,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["DashBoard"],
)
@jwt_required()
@permission_required("dash_board_donations", "acessar")
def donations_per_type():
    """Retorna quantidade de valores arrecados de forma avulsa e recorrente"""
    try:
        per_type = DonatinonsPerType(db)
        response = response_handler(per_type.execute(), save_logs=False)
        return response
    except Exception as e:
        response_error = errors_handler(e, save_logs=True)
        return response_error


@dash_board_donations.get("/total-donations-value")
@api.validate(
    query=DashboardFilterQuery,
    resp=Response(
        HTTP_200=TotalDonations,
        HTTP_403=DefaultErrorResponseSchema,
        HTTP_404=DefaultErrorResponseSchema,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["DashBoard"],
)
@jwt_required()
@permission_required("dash_board_donations", "acessar")
def amount_donations():
    """
    Retorna total de doações do ano atual
    """
    try:
        get_values = CardTotalValue(db)
        response = response_handler(get_values.execute())
        return response
    except Exception as e:
        response_error = errors_handler(e)
        return response_error


@dash_board_donations.get("/total-donations-mes-atual")
@api.validate(
    query=None,
    resp=Response(
        # HTTP_200=TotalDonations,
        HTTP_403=DefaultErrorResponseSchema,
        HTTP_404=DefaultErrorResponseSchema,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["DashBoard"],
)
@jwt_required()
@permission_required("doacoes", "acessar")
def total_mes_atual():
    """Retorna quantidade de doações do mês atual"""
    try:
        get_values_actual_month = TotalDonationsActualMonth(db)
        response = response_handler(get_values_actual_month.execute())
        return response
    except Exception as e:
        response_error = errors_handler(e)
        return response_error


@dash_board_donations.get("/total-donations-dia-atual")
@api.validate(
    query=None,
    resp=Response(
        HTTP_200=TotalDonations,
        HTTP_403=DefaultErrorResponseSchema,
        HTTP_404=DefaultErrorResponseSchema,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["DashBoard"],
)
@jwt_required()
@permission_required("doacoes", "acessar")
def total_dia_atual():
    """Retorna o total de doações do dia atual"""
    try:
        get_actual_day = TotalDonationsActualDay(db)
        response = response_handler(get_actual_day.execute())
        return response
    except Exception as e:
        response_error = errors_handler(e)
        return response_error


@dash_board_donations.get("/total-daily-donations-value")
@api.validate(
    query=DashboardFilterQuery,
    resp=Response(
        HTTP_200=TotalDonationsDaily,
        HTTP_403=DefaultErrorResponseSchema,
        HTTP_404=DefaultErrorResponseSchema,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["DashBoard"],
)
@jwt_required()
@permission_required("dash_board_donations", "acessar")
def total_daily_donations():
    """
    Retorna valor total de doações no dia atual
    """
    try:
        card_total_dia = TotalDailyDonations(db)
        response = response_handler(card_total_dia.execute())
        return response
    except Exception as e:
        response_error = errors_handler(e)
        return response_error


@dash_board_donations.get("/doacoes-media-mensal")
@api.validate(
    query=None,
    resp=Response(
        HTTP_200=MediaMensal,
        HTTP_403=DefaultErrorResponseSchema,
        HTTP_404=DefaultErrorResponseSchema,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["DashBoard"],
)
@jwt_required()
@permission_required("doacoes", "acessar")
def media_mensal():
    """Traz a média do valor das doações mensal e a média da quantidade de registros mensal"""
    try:
        media_mensal = MediaMensalDonations(db)
        response = response_handler(media_mensal.execute())
        return response
    except Exception as e:
        error_response = errors_handler(e)
        return error_response


@dash_board_donations.get("/doacoes-media-diaria")
@api.validate(
    query=None,
    resp=Response(
        # HTTP_200=MediaDiaria,
        HTTP_403=DefaultErrorResponseSchema,
        HTTP_404=DefaultErrorResponseSchema,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["DashBoard"],
)
@jwt_required()
@permission_required("doacoes", "acessar")
def media_diaria():
    """Traz média de doações diária por dia da semana"""
    try:
        media_diaria = MediaDiariaDonations(db)
        response = response_handler(media_diaria.execute())
        return response
    except Exception as e:
        response_error = errors_handler(e)
        return response_error


@dash_board_donations.get("/doacoes-diaria-per-hour")
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
@permission_required("dash_board_donations", "acessar")
def doantions_per_hors_daily():
    """Retorna os valores de doações do dia por hora doa dia!"""
    try:
        get_data_diario = DonationsPerHoursNow(db)
        response = response_handler(get_data_diario.execute())
        return response
    except Exception as e:
        response_error = errors_handler(e)
        return response_error


@dash_board_donations.get("/user-total-donation/<int:user_id>")
@api.validate(
    resp=Response(
        HTTP_200=UserTotalDonations,
        HTTP_403=DefaultErrorResponseSchema,
        HTTP_404=DefaultErrorResponseSchema,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["DashBoard"],
)
@jwt_required()
@permission_required("dash_board_users", "acessar")
def user_total_donations(user_id):
    """Retorna total doado por usuário!"""
    try:
        get_all_user_donaitions = UserTotalDonation(db, user_id)
        response = response_handler(get_all_user_donaitions.execute())
        return response
    except Exception as e:
        response_error = errors_handler(e)
        return response_error


@dash_board_donations.get("/user-donation-actual-month/<int:user_id>")
@api.validate(
    resp=Response(
        HTTP_200=DonationItem,
        HTTP_403=DefaultErrorResponseSchema,
        HTTP_404=DefaultErrorResponseSchema,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["DashBoard"],
)
@jwt_required()
@permission_required("dash_board_users", "acessar")
def donations_user_actual_month(user_id):
    """Retorna o total de doações do mês por usuário"""
    try:
        get_user_donations = DonationsUserActualMonth(db, user_id)
        response = response_handler(get_user_donations.execute())
        return response
    except Exception as e:
        response_error = errors_handler(e)
        return response_error


@dash_board_donations.get("/donations-mes-recorrentes")
@api.validate(
    resp=Response(
        # HTTP_200=DonationActualMonth,
        HTTP_403=DefaultErrorResponseSchema,
        HTTP_404=DefaultErrorResponseSchema,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["DashBoard"],
)
@jwt_required()
@permission_required("doacoes", "acessar")
def donations_mes_recorrente():
    """Retorna valor total efetuadas e não efetuadas por mês"""
    try:
        total_recorrentes_mes_atual = DonationsMesRecorrente(db)
        response = response_handler(total_recorrentes_mes_atual.execute())
        return response
    except Exception as e:
        response_error = errors_handler(e)
        return response_error


@dash_board_donations.get("/actual-donations-recorrentes")
@api.validate(
    resp=Response(
        # HTTP_200=DonationActualMonth,
        HTTP_403=DefaultErrorResponseSchema,
        HTTP_404=DefaultErrorResponseSchema,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["DashBoard"],
)
@jwt_required()
@permission_required("dash_board_users", "acessar")
def donations_mes_atual_apuradas():
    """Retorna doações recorrentes apuradas mês a mês"""
    try:

        rec_actual_month = DonationsMesAtualApuradas(db)
        response = response_handler(rec_actual_month.execute())
        return response
    except Exception as e:
        response_error = errors_handler(e)
        return response_error
