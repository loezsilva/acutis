import logging
from exceptions.errors_handler import errors_handler
from flask import Blueprint, jsonify
from spectree import Response
from services.factories import file_service_factory
from utils.response import DefaultErrorResponseSchema
from models import LandPage, Campanha

from builder import api, db
from handlers.campaigns.landing_pages.register.register_landpage import (
    RegisterLandPage,
)
from handlers.campaigns.landing_pages.register.update_register_landpage import (
    UpdateRegisterLandPage,
)

landpage_controller = Blueprint(
    "landpage_controller", __name__, url_prefix="/landpage"
)


@landpage_controller.get("/<int:landpage_id>")
@api.validate(
    resp=Response(
        HTTP_200=None,
        HTTP_404=DefaultErrorResponseSchema,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Landing Page"],
)
def get_landpage_by_id(landpage_id):
    """
    Retorna o cadastro de uma landing page pelo ID
    """
    try:

        s3_client = file_service_factory()

        landpage = db.session.get(LandPage, landpage_id)
        if not landpage:
            response = {
                "error": f"Landing page com id {landpage_id} não encontrada."
            }, 404

            return response

        preenchimento_foto = False
        label_foto = None

        if landpage.campanha_id:
            campanha = db.session.get(Campanha, landpage.campanha_id)
            preenchimento_foto = campanha.preenchimento_foto
            label_foto = campanha.label_foto

        response = {
            "id": landpage.id,
            "campanha_id": landpage.campanha_id,
            "banner": (
                s3_client.get_public_url(landpage.banner)
                if landpage.banner != None
                else True
            ),
            "titulo": landpage.titulo,
            "descricao": landpage.descricao,
            "tipo_cadastro": landpage.tipo_cadastro,
            "data_criacao": landpage.data_criacao,
            "texto_pos_registro": landpage.texto_pos_registro,
            "texto_email_pos_registro": landpage.texto_email_pos_registro,
            "preenchimento_foto": preenchimento_foto,
            "label_foto": label_foto,
        }

        return jsonify(response), 200
    except Exception as err:
        logging.error(f"{type(err)} - {err}")
        response = {
            "error": "Ocorreu um erro ao retornar o cadastro da landing page."
        }, 500

        return response


@landpage_controller.post("/register")
@api.validate(
    form=None,
    resp=Response(
        HTTP_200=None,
        HTTP_404=DefaultErrorResponseSchema,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Landing Page"],
)
def register_user_by_campaign():
    try:
        register_by_landpage = RegisterLandPage()
        return register_by_landpage.execute()
    except Exception as err:
        raise errors_handler(err)


@landpage_controller.put("/update")
@api.validate(
    form=None,
    resp=Response(
        HTTP_200=None,
        HTTP_404=DefaultErrorResponseSchema,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Landing Page"],
)
def update_user_by_landpage():
    try:
        update_by_landpage = UpdateRegisterLandPage()
        return update_by_landpage.execute()
    except Exception as err:
        raise errors_handler(err)
