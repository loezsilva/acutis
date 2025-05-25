from flask import Blueprint
from flask_jwt_extended import jwt_required
from builder import api
from handlers.mensageria.get.card_emails_sent import CardEmailsSent
from handlers.mensageria.get.get_emails_sent import GetEmailsSent
from handlers.mensageria.get.get_stats_emails import GetStatsEmails
from handlers.mensageria.get.stats_by_browser import StatsBrowser
from handlers.mensageria.get.stats_by_device import StatsDevice
from handlers.mensageria.get.stats_by_geolocalizacao import StatsLocation
from handlers.mensageria.post.create_type_email import CreateTypeEmail
from models.schemas.mensageria.form_validatior import CreateTypeEmailForm
from models.schemas.mensageria.query_validator import StatsByQuery
from utils.response import DefaultResponseSchema, DefaultErrorResponseSchema, response_handler
from spectree import Response
from exceptions.errors_handler import errors_handler
from builder import db
from utils.verify_permission import permission_required


mensageria_controller = Blueprint(
    "mensageria_controller", __name__, url_prefix="/mensageria"
)   

@mensageria_controller.post("/create-type-email")
@jwt_required()
@permission_required("mensageria", "criar")
@api.validate(
    json=CreateTypeEmailForm,
    resp=Response(
        HTTP_200=DefaultResponseSchema,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Mensageria"],
)
def create_tipo_email():
    """Create a new tipo email"""
    
    try:
        create = CreateTypeEmail(db)
        return response_handler(create.execute(), save_logs=True)
    except Exception as er:
        return errors_handler(er)
    

@mensageria_controller.get("/estatisticas-por-periodo")
@jwt_required()
@permission_required("mensageria", "acessar")
@api.validate(
    query=StatsByQuery,
    resp=Response(
        HTTP_200=None,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Mensageria"],
)
def get_stats_emails():
    """Lista estatisticas de emails"""
    
    try:
        get_stats_emails = GetStatsEmails()
        return response_handler(get_stats_emails.execute(), save_logs=True)
    except Exception as er:
        return errors_handler(er)
    
    
@mensageria_controller.get("/estatisticas-por-dispositivo")
@jwt_required()
@permission_required("mensageria", "acessar")
@api.validate(
    query=StatsByQuery,
    resp=Response(
        HTTP_200=None,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Mensageria"],
)
def get_stats_emails_by_device():
    """Lista estatisticas de emails por dispositivo"""
    
    try:
        stats_device = StatsDevice()
        return response_handler(stats_device.execute(), save_logs=True)
    except Exception as er:
        return errors_handler(er)
    
    
@mensageria_controller.get("/estatisticas-por-navegador")
@jwt_required()
@permission_required("mensageria", "acessar")
@api.validate(
    query=StatsByQuery,
    resp=Response(
        HTTP_200=None,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Mensageria"],
)
def get_stats_emails_by_browser():
    """Lista estatisticas de emails por navegador"""
    
    try:
        stats_browser = StatsBrowser()
        return response_handler(stats_browser.execute(), save_logs=True)
    except Exception as er:
        return errors_handler(er)
    
@mensageria_controller.get("/estatisticas-por-geolocalizacao")
@jwt_required()
@permission_required("mensageria", "acessar")
@api.validate(
    query=StatsByQuery,
    resp=Response(
        HTTP_200=None,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Mensageria"],
)
def get_stats_emails_by_location():
    """Lista estatisticas de emails por geolocalizacao"""
    
    try:
        stats_location = StatsLocation()
        return response_handler(stats_location.execute(), save_logs=True)
    except Exception as er:
        return errors_handler(er)
    
    
@mensageria_controller.get("/lista-de-emails-enviados")
@jwt_required()
@permission_required("mensageria", "acessar")
@api.validate(
    query=None,
    resp=Response(
        HTTP_200=None,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Mensageria"],
)
def get_emails_sent():
    """Lista emails enviados"""
    
    try:
        get_emails = GetEmailsSent(db)
        return response_handler(get_emails.execute(), save_logs=True)
    except Exception as er:
        return errors_handler(er)
    
    
@mensageria_controller.get("/card-emails-enviados")
@jwt_required()
@permission_required("mensageria", "acessar")
@api.validate(
    query=None,
    resp=Response(
        HTTP_200=None,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Mensageria"],
)
def card_emails_sent():
    """Lista emails enviados"""
    try:
        card_emails = CardEmailsSent(db)
        return response_handler(card_emails.execute(), save_logs=True)
    except Exception as er:
        return errors_handler(er)