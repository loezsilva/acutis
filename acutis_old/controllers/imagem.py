from typing import List

from exceptions.errors_handler import errors_handler
from handlers.imagens.get_image_use_campaign import GetImageUserCampaign
from flask import Blueprint
from flask_jwt_extended import jwt_required
from pydantic import BaseModel
from spectree import Response, BaseFile

from utils.response import (
    response_handler,
)
from builder import api

image_controller = Blueprint(
    "image_controller", __name__, url_prefix="/images"
)


class UploadImageResponseSchema(BaseModel):
    filename: str


class UploadImageSchema(BaseModel):
    image: BaseFile


class DeletedImagesSchema(BaseModel):
    deletadas: List[str]
    nao_deletadas: List[str]


class UnusedImageSchema(BaseModel):
    root: DeletedImagesSchema


class ImagesListResponseSchema(BaseModel):
    images: List[str]


class ImageResponseSchema(BaseModel):
    image_url: str


@image_controller.get("/user-photo-campaign")
@api.validate(
    resp=Response(HTTP_200=None, HTTP_404=None, HTTP_500=None),
    tags=["Imagens"],
)
@jwt_required()
def get_user_photo_campaign():
    """
    Retorna a foto do usuário na campanha pelo ID do usuário
    """
    try:
        get_image_campaign = GetImageUserCampaign()
        return response_handler(get_image_campaign.execute())
    except Exception as e:
        return errors_handler(e)
