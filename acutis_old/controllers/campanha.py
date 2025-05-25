from flask_jwt_extended import jwt_required
from flask import Blueprint
from flask.globals import request
from spectree import Response
from exceptions.errors_handler import errors_handler
from handlers.campaigns.campaign_details import CampaignsDetails
from handlers.campaigns.create_campaign import CreateCampaign
from handlers.campaigns.get.get_public_campaign import GetPublicCampaign
from handlers.campaigns.get.get_registers_of_campaign import (
    GetRegisterOfCampaign,
)
from handlers.campaigns.get_all.get_all_public_campaigns import (
    GetAllPublicCampaigns,
)
from handlers.campaigns.update_campaign import UpdateCampaign
from handlers.campaigns.delete_campaign import DeleteCampaign
from handlers.campaigns.campaign_get_by_id import CampaignGetById
from handlers.campaigns.campaigns_get_all import GetAllCampaigns
from models.campanha import (
    CampaignCreateSchema,
    CampaignQuerySchema,
)
from services.factories import file_service_factory
from utils.response import (
    DefaultResponseSchema,
    DefaultErrorResponseSchema,
    ErrorWithLogResponseSchema,
    response_handler,
)
from models import (
    Campanha,
)
from builder import api, db
from utils.verify_permission import permission_required

campaign_controller = Blueprint(
    "campaign_controller", __name__, url_prefix="/campaigns"
)


@campaign_controller.post("")
@api.validate(
    json=CampaignCreateSchema,
    resp=Response(
        HTTP_201=DefaultResponseSchema,
        HTTP_400=DefaultErrorResponseSchema,
        HTTP_403=DefaultErrorResponseSchema,
        HTTP_404=DefaultErrorResponseSchema,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Campanhas"],
)
@jwt_required()
@permission_required("campanha", "criar")
def create_campaign():
    """
    Cadastra uma nova campanha
    """
    try:
        create_campaign = CreateCampaign()
        response = response_handler(create_campaign.execute(), save_logs=True)
        return response
    except Exception as err:
        error_response = error_response(err, save_logs=True)
        return error_response


@campaign_controller.put("/<int:fk_campanha_id>")
@api.validate(
    json=CampaignCreateSchema,
    resp=Response(
        HTTP_200=DefaultResponseSchema,
        HTTP_400=DefaultErrorResponseSchema,
        HTTP_403=DefaultErrorResponseSchema,
        HTTP_404=DefaultErrorResponseSchema,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Campanhas"],
)
@jwt_required()
@permission_required("campanha", "editar")
def update_campaign(fk_campanha_id: int):
    """
    Atualiza o cadastro de uma campanha pelo ID
    """
    try:
        update_campaign = UpdateCampaign(fk_campanha_id)
        response = response_handler(update_campaign.execute(), save_logs=True)
        return response

    except Exception as err:
        response_error = errors_handler(err, save_logs=True)
        return response_error


@campaign_controller.get("/campanhas-publicas")
@api.validate(resp=Response(HTTP_200=None, HTTP_500=None), tags=["Campanhas"])
def get_all_public_campaigns():
    """Listagem das campanhas publicas para benfeitores"""
    try:
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)
        s3_client = file_service_factory()

        get_campanhas = GetAllPublicCampaigns(db, s3_client, page, per_page)
        response = response_handler(get_campanhas.execute(), save_logs=False)
        return response

    except Exception as exception:
        response = errors_handler(exception, save_logs=False)
        return response


@campaign_controller.get("/campanha-publica/<int:fk_campanha_id>")
@api.validate(
    resp=Response(HTTP_200=None, HTTP_404=None, HTTP_500=None),
    tags=["Campanhas"],
)
@jwt_required(optional=True)
def get_public_campaign(fk_campanha_id: int):
    try:
        s3_client = file_service_factory()
        get_campanha = GetPublicCampaign(db, s3_client)
        response = response_handler(
            get_campanha.execute(fk_campanha_id), save_logs=False
        )
        return response

    except Exception as exception:
        response = errors_handler(exception, save_logs=False)
        return response


@campaign_controller.delete("/<int:campaign_id>")
@api.validate(
    resp=Response(
        HTTP_200=DefaultResponseSchema,
        HTTP_403=DefaultErrorResponseSchema,
        HTTP_404=DefaultErrorResponseSchema,
        HTTP_500=ErrorWithLogResponseSchema,
    ),
    tags=["Campanhas"],
)
@jwt_required()
@permission_required("campanha", "deletar")
def delete_campaign(campaign_id):
    """
    Deleta o cadastro de uma campanha pelo ID
    """
    try:
        delete_campaign = DeleteCampaign(campaign_id)
        response = response_handler(delete_campaign.execute(), save_logs=True)
        return response
    except Exception as err:
        response_error = errors_handler(err, save_logs=True)
        return response_error


@campaign_controller.get("/registers-of-campaign/<int:campaign_id>")
@jwt_required()
@permission_required("campanha", "acessar")
@api.validate(
    query=CampaignQuerySchema,
    resp=Response(
        HTTP_200=None,
        HTTP_403=DefaultErrorResponseSchema,
        HTTP_404=DefaultErrorResponseSchema,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Campanhas"],
)
def registers_of_campaigns(campaign_id):
    """Busca todos os registros pela campanha"""
    try:
        get_registers = GetRegisterOfCampaign(db, campaign_id)
        response = response_handler(get_registers.execute(), save_logs=True)
        return response
    except Exception as e:
        return errors_handler(e)


@campaign_controller.get("/admin/<int:campaign_id>")
@jwt_required()
@permission_required("campanha", "acessar")
@api.validate(
    query=CampaignQuerySchema,
    resp=Response(
        HTTP_200=None,
        HTTP_403=DefaultErrorResponseSchema,
        HTTP_404=DefaultErrorResponseSchema,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Campanhas"],
)
def get_campaign(campaign_id):
    """
    Retorna o cadastro de uma campanha pelo ID
    """
    try:

        get_by_id = CampaignGetById(campaign_id)
        response = response_handler(get_by_id.execute(), save_logs=True)
        return response

    except Exception as err:
        response_error = errors_handler(err, save_logs=True)
        return response_error


@campaign_controller.get("")
@api.validate(
    query=None,
    resp=Response(HTTP_200=None, HTTP_403=None, HTTP_404=None, HTTP_500=None),
    tags=["Campanhas"],
)
@jwt_required()
@permission_required("campanha", "acessar")
def get_all_campaigns():
    """
    Retorna a lista de todas as campanhas com paginação e filtros adicionais
    """
    try:
        get_all_campaigns = GetAllCampaigns(request)
        response = response_handler(
            get_all_campaigns.execute(), save_logs=True
        )
        return response

    except Exception as err:
        response_error = response_handler(err, save_logs=True)
        return response_error


@campaign_controller.get("/users-donations-per-campaign")
@jwt_required()
@api.validate(
    query=None,
    resp=Response(
        HTTP_200=None,
        HTTP_403=DefaultErrorResponseSchema,
        HTTP_404=DefaultErrorResponseSchema,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Campanhas"],
)
@permission_required("campanha", "acessar")
def users_donations_per_campaign():
    """Retorna a contabilidade de cadastros e doações por campanha."""
    try:

        campaign_details = CampaignsDetails(db)
        response = response_handler(campaign_details.execute(), save_logs=True)

        return response

    except Exception as err:
        response_error = errors_handler(err, save_logs=True)
        return response_error


@campaign_controller.get("/info")
@jwt_required()
@api.validate(resp=Response(HTTP_200=None, HTTP_500=None), tags=["Campanhas"])
def info_campaigns():
    """Retorna o ID e o Titulo das campanhas"""
    try:
        filter_objetivo = request.args.get("objetivo", None, type=str)

        campanhas = (
            Campanha.query.with_entities(
                Campanha.id, Campanha.titulo, Campanha.objetivo
            )
            .filter(
                (
                    Campanha.objetivo == filter_objetivo
                    if filter_objetivo
                    else True
                ),
                Campanha.contabilizar_doacoes == 1,
            )
            .all()
        )

        result = {
            "campanhas": [
                {
                    "id": campanha.id,
                    "titulo": campanha.titulo,
                    "objetivo": campanha.objetivo,
                }
                for campanha in campanhas
            ]
        }

        response = response_handler(result, save_logs=True)
        return response, 200

    except Exception as err:
        response_error = errors_handler(err, save_logs=True)
        response = response_error
